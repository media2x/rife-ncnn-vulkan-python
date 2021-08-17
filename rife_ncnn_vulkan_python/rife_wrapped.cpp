#include "rife_wrapped.h"

RifeWrapped::RifeWrapped(int gpuid, bool _tta_mode, bool _uhd_mode,
                         int _num_threads, bool _rife_v2)
    : RIFE(gpuid, _tta_mode, _uhd_mode, _num_threads, _rife_v2)
{
}

int RifeWrapped::load(const StringType &modeldir)
{
#if _WIN32
    return RIFE::load(*modeldir.wstr);
#else
    return RIFE::load(*modeldir.str);
#endif
}

int RifeWrapped::process(const Image &inimage0, const Image &inimage1,
                         float timestep, Image outimage)
{
    int c = inimage0.elempack;
    ncnn::Mat inimagemat0 =
        ncnn::Mat(inimage0.w, inimage0.h, (void *)inimage0.data, (size_t)c, c);
    ncnn::Mat inimagemat1 =
        ncnn::Mat(inimage1.w, inimage1.h, (void *)inimage1.data, (size_t)c, c);
    ncnn::Mat outimagemat =
        ncnn::Mat(outimage.w, outimage.h, (void *)outimage.data, (size_t)c, c);
    return RIFE::process(inimagemat0, inimagemat1, timestep, outimagemat);
}
int get_gpu_count() { return ncnn::get_gpu_count(); }
