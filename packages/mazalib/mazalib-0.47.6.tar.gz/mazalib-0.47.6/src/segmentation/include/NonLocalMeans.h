#pragma once

/*********************************************************************************************************************************************************
 *
 * Location: Helmholtz-Zentrum fuer Material und Kuestenforschung,
 *Max-Planck-Strasse 1, 21502 Geesthacht Author: Stefan Bruns Contact:
 *bruns@nano.ku.dk Edited by: Roman V. Vasilyev, Mail.ru Group Contact:
 *vasilyev.rw@gmail.com
 *
 * License: TBA
 *
 *********************************************************************************************************************************************************/

// THIS IS A CPU VERSION

class NonLocalMeans {
public:
  static int *nlm_denoise(const int *data_ptr, int shape[3], int n_iterations,
                          int search_radius, bool verbose);
};
