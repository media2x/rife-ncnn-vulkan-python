%module rife_ncnn_vulkan_wrapper

%include "cpointer.i"
%include "carrays.i"
%include "std_string.i"
%include "std_wstring.i"
%include "stdint.i"
%include "pybuffer.i"

%pybuffer_mutable_string(unsigned char *d);
%pointer_functions(std::string, str_p);
%pointer_functions(std::wstring, wstr_p);

%{
    #include "rife.h"
    #include "rife_wrapped.h"
%}

class RIFE
{
  public:
    RIFE(int gpuid, bool tta_mode = false, bool uhd_mode = false,
         int num_threads = 1, bool rife_v2 = false);
    ~RIFE();
};

%include "rife_wrapped.h"
