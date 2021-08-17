#ifndef RIFE_NCNN_VULKAN_RIFEWRAPPER_H
#define RIFE_NCNN_VULKAN_RIFEWRAPPER_H
#include "rife.h"

// wrapper class of ncnn::Mat
typedef struct Image {
    unsigned char *data;
    int w;
    int h;
    int elempack;
    Image(unsigned char *d, int w, int h, int channels)
    {
        this->data = d;
        this->w = w;
        this->h = h;
        this->elempack = channels;
    }

} Image;

union StringType {
    std::string *str;
    std::wstring *wstr;
};

class RifeWrapped : public RIFE
{
  public:
    RifeWrapped(int gpuid, bool _tta_mode, bool _uhd_mode, int _num_threads,
                bool _rife_v2);
    int load(const StringType &modeldir);
    int process(const Image &inimage0, const Image &inimage1, float timestamp,
                Image outimage);
};

int get_gpu_count();
#endif // RIFE_NCNN_VULKAN_RIFEWRAPPER_H
