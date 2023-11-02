/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Enum Utility Definitions                                                   *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|* From: ArmSMEOps.td                                                         *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace arm_sme {
::llvm::StringRef stringifyCombiningKind(CombiningKind val) {
  switch (val) {
    case CombiningKind::Add: return "add";
    case CombiningKind::Sub: return "sub";
  }
  return "";
}

::std::optional<CombiningKind> symbolizeCombiningKind(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::std::optional<CombiningKind>>(str)
      .Case("add", CombiningKind::Add)
      .Case("sub", CombiningKind::Sub)
      .Default(::std::nullopt);
}
::std::optional<CombiningKind> symbolizeCombiningKind(uint32_t value) {
  switch (value) {
  case 0: return CombiningKind::Add;
  case 1: return CombiningKind::Sub;
  default: return ::std::nullopt;
  }
}

} // namespace arm_sme
} // namespace mlir

namespace mlir {
namespace arm_sme {
::llvm::StringRef stringifyTileSliceLayout(TileSliceLayout val) {
  switch (val) {
    case TileSliceLayout::Horizontal: return "horizontal";
    case TileSliceLayout::Vertical: return "vertical";
  }
  return "";
}

::std::optional<TileSliceLayout> symbolizeTileSliceLayout(::llvm::StringRef str) {
  return ::llvm::StringSwitch<::std::optional<TileSliceLayout>>(str)
      .Case("horizontal", TileSliceLayout::Horizontal)
      .Case("vertical", TileSliceLayout::Vertical)
      .Default(::std::nullopt);
}
::std::optional<TileSliceLayout> symbolizeTileSliceLayout(uint32_t value) {
  switch (value) {
  case 0: return TileSliceLayout::Horizontal;
  case 1: return TileSliceLayout::Vertical;
  default: return ::std::nullopt;
  }
}

} // namespace arm_sme
} // namespace mlir

