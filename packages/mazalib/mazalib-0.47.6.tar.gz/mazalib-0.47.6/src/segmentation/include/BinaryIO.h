#pragma once

#include <iostream>
#include <string>

template <typename CONTAINER_TYPE>
void read_binary(std::string filename, int width, int height,
                 CONTAINER_TYPE &input_image) {
  input_image.reserve(width * height);
  FILE *f = fopen(filename.c_str(), "rb");
  for (int y = 0; y < height; y++) {
    for (int x = 0; x < width; x++) {
      int px = fgetc(f);
      input_image.push_back(px);
    }
  }
  fclose(f);
}

template <typename CONTAINER_TYPE>
void read_binary(std::string filename, size_t len,
                 CONTAINER_TYPE &input_image) {
  input_image.reserve(len);
  FILE *f = fopen(filename.c_str(), "rb");
  for (size_t y = 0UL; y < len; y++) {
    int px = fgetc(f);
    input_image.push_back(px);
  }
  fclose(f);
}

template <typename CONTAINER_TYPE>
void write_binary(const CONTAINER_TYPE &output_image, size_t len,
                  const std::string &filename) {
  FILE *f = fopen(filename.c_str(), "wb");
  for (size_t i = 0UL; i < len; i++) {
    fputc(output_image[i], f);
  }
  fclose(f);
}
