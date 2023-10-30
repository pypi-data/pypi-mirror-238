#pragma once

#include "BinaryIO.h"
#include "DynamicArray.h"
#include "IntegralImage.h"
#include "LatticeModel.h"
#include "LogFile.h"
#include "threshold.h"


#include <cmath>
#include <cstring>
#include <queue>
#include <unordered_map>
#include <vector>

struct CACSettings {
  CACSettings(){};
  float AlphaI;
  float AlphaG;
  float G0;
};

class CACFiller {
  struct SurfaceVoxel {
    int propagating_label;
    float speed;
    float current_value;
    float threshold;

    SurfaceVoxel(int _label, float _speed, float _current_value,
                 float _threshold)
        : propagating_label{_label}, speed{_speed},
          current_value{_current_value}, threshold{_threshold} {}

    SurfaceVoxel() : SurfaceVoxel{0, 0.1f, 0.0f, 1.0f} {}
  };

  using sv_chain_t = std::vector<SurfaceVoxel>;
  using sv_chain_iterator_t = typename sv_chain_t::iterator;

  using front_t = std::unordered_map<size_t, sv_chain_t>;
  using front_iterator_t = typename front_t::iterator;
  using del_map_t = std::unordered_map<size_t, int>;
  using del_iterator_t = typename del_map_t::iterator;

public:
  CACFiller(const std::vector<int> &_img, std::vector<int> &_seg,
            std::vector<int> &_sobel, const size_t _dim_x, const size_t _dim_y,
            const size_t _dim_z, const int _L, const int _H,
            const CACSettings &_settings, int undef = 255,
            const float _speed = 0.1)
      : img{_img}, seg{_seg}, sobel{_sobel}, dim_x{_dim_x}, dim_y{_dim_y},
        dim_z{_dim_z}, len{_dim_x * _dim_y * _dim_z}, default_speed{_speed},
        n_steps{0UL}, ortho{false}, L{_L}, H{_H}, settings{_settings},
        undef_(undef) {}

  ~CACFiller() {}

  void toggle_ortho(bool flag) { ortho = flag; }

  void clear() {
    for (size_t i = 0; i < len; i++) {
      seg[i] = undef_;
    }
  }

  void output(std::string filename) { write_binary(seg, len, filename); }

  void init_front() {
    for (size_t pos = 0; pos < len; pos++) {
      if (seg[pos] != undef_) {
        check_neighbors(pos, seg[pos], 0.0);
      }
    }
    commit_pending_add();
  }

  void step_up() {
    front_forward();
    commit_pending();
    n_steps++;
    // std::cout << n_steps << " passed. Front size = " << front.size() <<
    // std::endl;
  }

  void step_n(size_t n) {
    for (size_t s = 0; s < n; s++) {
      step_up();
    }
  }

  void reset() {
    commit_pending();
    front.clear();
  }

  void propagate() {
    size_t undef_cnt{0UL};
    reset();
    init_front();
    while (!front.empty()) {
      step_up();
    }
  }

private:
  void front_forward() {
    float max_speed = 0.0;
    size_t concurrent_cnt = 0UL;
    for (front_iterator_t it = front.begin(); it != front.end(); it++) {
      sv_chain_t chain = it->second;
      for (const SurfaceVoxel &sv : chain) {
        max_speed = sv.speed > max_speed ? sv.speed : max_speed;
      }
      if (chain.size() > 1UL) {
        concurrent_cnt++;
      }
    }
    // std::cout << "Max speed = " << max_speed << std::endl;
    // std::cout << "Concurrent percentage = " << 100.0f * concurrent_cnt /
    // front.size() << "%" << std::endl;

    for (front_iterator_t it = front.begin(); it != front.end(); it++) {
      size_t position = it->first;
      increment_values(std::move(it), max_speed);
      sv_chain_t chain = it->second;

      SurfaceVoxel overgrown_one;
      if (select_overgrown(std::move(chain), overgrown_one)) {
        pending_delete.emplace(position, overgrown_one.propagating_label);
        float shift = overgrown_one.current_value - overgrown_one.threshold;
        check_neighbors(position, overgrown_one.propagating_label, shift);
      }
    }
  }

  void increment_values(front_iterator_t &&it, float max_speed) {
    size_t chain_len = it->second.size();
    for (size_t idx = 0; idx < chain_len; idx++) {
      it->second[idx].current_value +=
          max_speed > 0.0 ? it->second[idx].speed / max_speed : 1.0f;
    }
  }

  bool select_overgrown(sv_chain_t &&chain, SurfaceVoxel &overgrown) {
    bool exceed{false};
    float max_shift{-std::numeric_limits<float>::epsilon()};
    for (const SurfaceVoxel &svoxel : chain) {
      float shift = svoxel.current_value - svoxel.threshold;
      if (shift >= max_shift) {
        max_shift = shift;
        overgrown = svoxel;
        exceed = true;
      }
    }
    return exceed;
  }

  void check_neighbors(size_t position, int label, float shift) {
    int k = static_cast<int>(position / (dim_x * dim_y));
    position -= k * dim_x * dim_y;
    int i = static_cast<int>(position / dim_x);
    int j = static_cast<int>(position - i * dim_x);

    for (int offset_k = -1; offset_k <= 1; offset_k++) {
      for (int offset_i = -1; offset_i <= 1; offset_i++) {
        for (int offset_j = -1; offset_j <= 1; offset_j++) {
          int pos_k = k + offset_k;
          int pos_i = i + offset_i;
          int pos_j = j + offset_j;
          if (offset_k == 0 && offset_i == 0 && offset_j == 0) {
            continue;
          }
          if (pos_k < 0 || pos_k >= dim_z || pos_i < 0 || pos_i >= dim_y ||
              pos_j < 0 || pos_j >= dim_x) {
            continue;
          }
          float threshold = static_cast<float>(sqrt(
              offset_k * offset_k + offset_i * offset_i + offset_j * offset_j));

          // Old method
          if (ortho && (threshold < 0.9 || threshold > 1.1)) {
            continue;
          }

          size_t neighbor_position =
              pos_k * dim_y * dim_x + pos_i * dim_x + pos_j;
          // std::cout << "Neighbors checking at position " << neighbor_position
          // << std::endl;

          if (seg[neighbor_position] == undef_) {
            SurfaceVoxel new_svx(
                label, speed(pos_k, pos_i, pos_j, label),
                shift > std::numeric_limits<float>::epsilon() ? shift : 0.0f,
                threshold);
            add_svoxel_if_new_or_better(pending_add, neighbor_position,
                                        std::move(new_svx));
          }
        }
      }
    }
  }

  void commit_pending() {
    commit_pending_delete();
    commit_pending_add();
  }

  void commit_pending_delete() {
    for (del_iterator_t it = pending_delete.begin(); it != pending_delete.end();
         it++) {
      auto position = it->first;
      auto label = it->second;
      seg[position] = label;
      front.erase(position);
    }
    pending_delete.clear();
  }

  sv_chain_iterator_t select_existing_svoxel(sv_chain_t &chain, int label) {
    for (sv_chain_iterator_t it = chain.begin(); it != chain.end(); it++) {
      if (it->propagating_label == label) {
        return it;
      }
    }
    return chain.end();
  }

  void add_svoxel_to_chain(sv_chain_t &chain, SurfaceVoxel &&new_svx) {
    sv_chain_iterator_t existing =
        select_existing_svoxel(chain, new_svx.propagating_label);
    if (existing == chain.end()) {
      chain.emplace_back(std::move(new_svx));
    } else if (existing->threshold - existing->current_value >
               new_svx.threshold - new_svx.current_value) {
      chain.erase(existing);
      chain.emplace_back(std::move(new_svx));
    }
  }

  void add_svoxel_if_new_or_better(front_t &target, size_t position,
                                   SurfaceVoxel &&new_svoxel) {
    if (target.count(position) == 0) {
      if (seg[position] == undef_) {
        sv_chain_t new_chain;
        new_chain.emplace_back(std::move(new_svoxel));
        target.emplace(position, std::move(new_chain));
      }
    } else {
      add_svoxel_to_chain(target.at(position), std::move(new_svoxel));
    }
  }

  void commit_pending_add() {
    for (front_iterator_t it = pending_add.begin(); it != pending_add.end();
         it++) {
      auto position = it->first;
      sv_chain_t &chain_to_add = it->second;

      for (SurfaceVoxel &new_svoxel : chain_to_add) {
        add_svoxel_if_new_or_better(front, position, std::move(new_svoxel));
      }
    }
    pending_add.clear();
  }

  float speed(int k, int i, int j, int label) {
    size_t position = dim_y * dim_x * k + dim_x * i + j;
    float Fg = 1.0f / (1.0f + pow((float)sobel[position] / settings.G0,
                                  settings.AlphaG));
    // Choose threshold of the opposite phase
    float Intensity = label == 0 ? (float)H : (float)L;
    float Fi =
        pow(abs((Intensity - img[position]) / (float)(H - L)), settings.AlphaI);
    return Fg * Fi;
  }

private:
  const std::vector<int> &img;
  std::vector<int> &seg;
  std::vector<int> &sobel;
  const size_t dim_x;
  const size_t dim_y;
  const size_t dim_z;
  const size_t len;
  float default_speed;
  size_t n_steps;
  bool ortho;
  const int L;
  const int H;
  const CACSettings &settings;
  int undef_{255};
  front_t front;
  del_map_t pending_delete;
  front_t pending_add;
};

class NewCACSegmentation : public LatticeModel {
  using container_type = typename std::vector<int>;
  using LatticeIterator = typename container_type::iterator;
  using LatticeConstIterator = typename container_type::const_iterator;

public:
  NewCACSegmentation(int undef = 255)
      : LatticeModel{LabelsCount}, nbh{nullptr}, undef_(undef) {
    int *nbh = new int[LabelsCount];
  }

  ~NewCACSegmentation() {
    if (nbh != nullptr) {
      delete[] nbh;
    }
  }

  void Perform(const container_type &Src, container_type &Conditional,
               Threshold<int, container_type> &Thresh, CACSettings &Settings,
               int Width, int Heigth, int Depth) {
    LogFile::WriteData("kriging.log", "Perform New CAC");
    this->mDepth = Depth;
    this->mWidth = Width;
    this->mHeight = Heigth;
    int shape[3] = {Width, Heigth, Depth};
    bool verbose = true;

    LogFile::WriteData("kriging.log", "Thresholding");
    int L = Thresh.Low();
    int H = Thresh.High();

    // std::cout << "Thresholding..." << std::endl;
    this->ConditionalImage2Labels(Src, Conditional, Thresh);
    this->Stats2L(Src, H, L, this->means[0], this->means[1], this->vars[0],
                  this->vars[1]);

    // std::cout << "Computing Sobel convolution..." << std::endl;
    container_type SobelImg(Src.size());
    SobelConvolution<uchar, container_type> Sobel;
    LogFile::WriteData("kriging.log", "Compute Sobel");
    Sobel.compute_sobel3D(Src, SobelImg, Width, Heigth, Depth);

    size_t undef_cnt{0UL};
    for (auto cit = Conditional.begin(); cit != Conditional.end(); cit++) {
      if (*cit == undef_) {
        undef_cnt++;
      }
    }

    // std::cout << "Start CAC propagation, undef count = " << undef_cnt <<
    // std::endl;
    CACFiller filler(Src, Conditional, SobelImg, Width, Heigth, Depth, L, H,
                     Settings, undef_, 0.1f);
    filler.toggle_ortho(true);
    filler.propagate();

    undef_cnt = 0UL;
    for (auto cit = Conditional.begin(); cit != Conditional.end(); cit++) {
      if (*cit == undef_) {
        undef_cnt++;
      }
    }
    // std::cout << "Finish CAC propagation, undef count = " << undef_cnt <<
    // std::endl;
  }

private:
  static const int LabelsCount = 2;
  int *nbh;
  int undef_{255};
};
