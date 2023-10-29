//
// License: MIT
//

#include <pybind11/pybind11.h>

#define PB11_WEAVER_DISABLE_clang_tooling_ExtractFunction_initiate
#define PB11_WEAVER_DISABLE_clang_tooling_RefactoringCallback_Ctor0
#define PB11_WEAVER_DISABLE_clang_tooling_RefactoringTool_applyAllReplacements
#define PB11_WEAVER_DISABLE_clang_tooling_Replacement_apply
#define PB11_WEAVER_DISABLE_clang_tooling_SourceFileCallbacks_handleBeginSource
#define PB11_WEAVER_DISABLE_applyAllReplacements_AddFunction
#define PB11_WEAVER_DISABLE_formatAndApplyAllReplacements_AddFunction
#define PB11_WEAVER_DISABLE_clang_tooling_RefactoringResultConsumer_handleError
#define PB11_WEAVER_DISABLE_clang_tooling_RefactoringResultConsumer_handle1
#define PB11_WEAVER_DISABLE_clang_tooling_AllTUsToolExecutor_Ctor1
#define PB11_WEAVER_DISABLE_clang_tooling_StandaloneToolExecutor_Ctor1
#define PB11_WEAVER_DISABLE_createRenameReplacements_AddFunction

#define PB11_WEAVER_DISABLE_clang_diff_SyntaxTree_getFilename // Not implemented
                                                              // in source
#include "_binding.cc.inc"

PYBIND11_MODULE(_C, m) {
  pybind11_weaver::CustomBindingRegistry reg;
  auto update_guard = DeclFn(m, reg);
}