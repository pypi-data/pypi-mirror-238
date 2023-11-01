#include <iostream>
#include <cmath>

#define NPY_PI        3.141592653589793238462643383279502884  /* pi */

#define PFB_NTAP 8

inline float sinc(float x) {
    if(x == 0.0) {
        return 1.0;
    } else {
        return sin(x*NPY_PI)/(x*NPY_PI);
    }
}

inline float hamming(float x) {
    return 0.543478261 - 0.456521739*cos(x);
}

/*
  Hanning window for use by the polyphase filter bank
*/

inline float hanning(float x) {
    return 0.5 - 0.5*cos(x);
}

int main() {
  int nChan = 32;
  
  int i;
  float *pfb;
  pfb = (float*) ::malloc(sizeof(float) * nChan*PFB_NTAP);
  for(i=0; i<nChan*PFB_NTAP; i++) {
      *(pfb + i) = sinc((i - nChan*PFB_NTAP/2.0 + 0.5)/nChan);
      *(pfb + i) *= hamming(2*NPY_PI*i/(nChan*PFB_NTAP));
      std::cout << i << ": " << *(pfb+i) << std::endl;
  }
  ::free(pfb);
  return 0;
}
