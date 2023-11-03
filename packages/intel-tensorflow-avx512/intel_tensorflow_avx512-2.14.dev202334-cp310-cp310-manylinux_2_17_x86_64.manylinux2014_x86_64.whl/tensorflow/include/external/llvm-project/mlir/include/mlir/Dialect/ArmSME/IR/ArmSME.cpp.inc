/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Op Definitions                                                             *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

#ifdef GET_OP_LIST
#undef GET_OP_LIST

::mlir::arm_sme::aarch64_sme_ld1b_horiz,
::mlir::arm_sme::aarch64_sme_ld1b_vert,
::mlir::arm_sme::aarch64_sme_ld1d_horiz,
::mlir::arm_sme::aarch64_sme_ld1d_vert,
::mlir::arm_sme::aarch64_sme_ld1h_horiz,
::mlir::arm_sme::aarch64_sme_ld1h_vert,
::mlir::arm_sme::aarch64_sme_ld1q_horiz,
::mlir::arm_sme::aarch64_sme_ld1q_vert,
::mlir::arm_sme::aarch64_sme_ld1w_horiz,
::mlir::arm_sme::aarch64_sme_ld1w_vert,
::mlir::arm_sme::aarch64_sme_mopa,
::mlir::arm_sme::aarch64_sme_mopa_wide,
::mlir::arm_sme::aarch64_sme_mops,
::mlir::arm_sme::aarch64_sme_mops_wide,
::mlir::arm_sme::aarch64_sme_smopa_wide,
::mlir::arm_sme::aarch64_sme_smops_wide,
::mlir::arm_sme::aarch64_sme_st1b_horiz,
::mlir::arm_sme::aarch64_sme_st1b_vert,
::mlir::arm_sme::aarch64_sme_st1d_horiz,
::mlir::arm_sme::aarch64_sme_st1d_vert,
::mlir::arm_sme::aarch64_sme_st1h_horiz,
::mlir::arm_sme::aarch64_sme_st1h_vert,
::mlir::arm_sme::aarch64_sme_st1q_horiz,
::mlir::arm_sme::aarch64_sme_st1q_vert,
::mlir::arm_sme::aarch64_sme_st1w_horiz,
::mlir::arm_sme::aarch64_sme_st1w_vert,
::mlir::arm_sme::aarch64_sme_sumopa_wide,
::mlir::arm_sme::aarch64_sme_sumops_wide,
::mlir::arm_sme::aarch64_sme_umopa_wide,
::mlir::arm_sme::aarch64_sme_umops_wide,
::mlir::arm_sme::aarch64_sme_usmopa_wide,
::mlir::arm_sme::aarch64_sme_usmops_wide,
::mlir::arm_sme::aarch64_sme_za_disable,
::mlir::arm_sme::aarch64_sme_za_enable,
::mlir::arm_sme::aarch64_sme_zero
#endif  // GET_OP_LIST

#ifdef GET_OP_CLASSES
#undef GET_OP_CLASSES


//===----------------------------------------------------------------------===//
// Local Utility Method Definitions
//===----------------------------------------------------------------------===//

namespace mlir {
namespace arm_sme {

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_ArmSME0(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!((((::llvm::isa<::mlir::VectorType>(type) &&
                                   ::llvm::cast<VectorType>(type).isScalable())) && ([](::mlir::Type elementType) { return (elementType.isSignlessInteger(1)); }(::llvm::cast<::mlir::ShapedType>(type).getElementType()))) && (((::llvm::isa<::mlir::VectorType>(type) &&
                                   ::llvm::cast<VectorType>(type).isScalable())) && (((::llvm::cast<::mlir::VectorType>(type).getNumElements()
                           == 16)) || ((::llvm::cast<::mlir::VectorType>(type).getNumElements()
                           == 8)) || ((::llvm::cast<::mlir::VectorType>(type).getNumElements()
                           == 4)) || ((::llvm::cast<::mlir::VectorType>(type).getNumElements()
                           == 2)) || ((::llvm::cast<::mlir::VectorType>(type).getNumElements()
                           == 1)))))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be scalable vector of 1-bit signless integer values of length 16/8/4/2/1, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_ArmSME1(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!((::llvm::isa<::mlir::LLVM::LLVMPointerType>(type)))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be LLVM pointer type, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_ArmSME2(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!((type.isSignlessInteger(32)))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be 32-bit signless integer, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_ArmSME3(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!((((::llvm::isa<::mlir::VectorType>(type) &&
                                   ::llvm::cast<VectorType>(type).isScalable())) && ([](::mlir::Type elementType) { return (elementType.isSignlessInteger(1)); }(::llvm::cast<::mlir::ShapedType>(type).getElementType()))) && (((::llvm::isa<::mlir::VectorType>(type) &&
                                   ::llvm::cast<VectorType>(type).isScalable())) && (((::llvm::cast<::mlir::VectorType>(type).getNumElements()
                           == 16)) || ((::llvm::cast<::mlir::VectorType>(type).getNumElements()
                           == 8)) || ((::llvm::cast<::mlir::VectorType>(type).getNumElements()
                           == 4)) || ((::llvm::cast<::mlir::VectorType>(type).getNumElements()
                           == 2)))))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be scalable vector of 1-bit signless integer values of length 16/8/4/2, but got " << type;
  }
  return ::mlir::success();
}

static ::mlir::LogicalResult __mlir_ods_local_type_constraint_ArmSME4(
    ::mlir::Operation *op, ::mlir::Type type, ::llvm::StringRef valueKind,
    unsigned valueIndex) {
  if (!((((::llvm::isa<::mlir::VectorType>(type) &&
                                   ::llvm::cast<VectorType>(type).isScalable())) && ([](::mlir::Type elementType) { return ((elementType.isSignlessInteger(8))) || ((elementType.isSignlessInteger(16))) || ((elementType.isBF16())) || ((elementType.isF16())) || ((elementType.isF32())) || ((elementType.isF64())); }(::llvm::cast<::mlir::ShapedType>(type).getElementType()))) && (((::llvm::isa<::mlir::VectorType>(type) &&
                                   ::llvm::cast<VectorType>(type).isScalable())) && (((::llvm::cast<::mlir::VectorType>(type).getNumElements()
                           == 16)) || ((::llvm::cast<::mlir::VectorType>(type).getNumElements()
                           == 8)) || ((::llvm::cast<::mlir::VectorType>(type).getNumElements()
                           == 4)) || ((::llvm::cast<::mlir::VectorType>(type).getNumElements()
                           == 2)))))) {
    return op->emitOpError(valueKind) << " #" << valueIndex
        << " must be scalable vector of 8-bit signless integer or 16-bit signless integer or bfloat16 type or 16-bit float or 32-bit float or 64-bit float values of length 16/8/4/2, but got " << type;
  }
  return ::mlir::success();
}
} // namespace arm_sme
} // namespace mlir
namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_ld1b_horiz definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_ld1b_horizGenericAdaptorBase::aarch64_sme_ld1b_horizGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.ld1b.horiz", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_ld1b_horizGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_ld1b_horizGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_ld1b_horizAdaptor::aarch64_sme_ld1b_horizAdaptor(aarch64_sme_ld1b_horiz op) : aarch64_sme_ld1b_horizAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_ld1b_horizAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_ld1b_horiz::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_ld1b_horiz::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_ld1b_horiz::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_ld1b_horiz::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_ld1b_horiz::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
}

void aarch64_sme_ld1b_horiz::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_ld1b_horiz::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 4u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_ld1b_horiz::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME1(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_ld1b_horiz::verifyInvariants() {
  return verifyInvariantsImpl();
}

void aarch64_sme_ld1b_horiz::getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
  for (::mlir::Value value : getODSOperands(1))
    effects.emplace_back(::mlir::MemoryEffects::Read::get(), value, ::mlir::SideEffects::DefaultResource::get());
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_ld1b_horiz)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_ld1b_vert definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_ld1b_vertGenericAdaptorBase::aarch64_sme_ld1b_vertGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.ld1b.vert", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_ld1b_vertGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_ld1b_vertGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_ld1b_vertAdaptor::aarch64_sme_ld1b_vertAdaptor(aarch64_sme_ld1b_vert op) : aarch64_sme_ld1b_vertAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_ld1b_vertAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_ld1b_vert::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_ld1b_vert::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_ld1b_vert::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_ld1b_vert::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_ld1b_vert::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
}

void aarch64_sme_ld1b_vert::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_ld1b_vert::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 4u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_ld1b_vert::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME1(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_ld1b_vert::verifyInvariants() {
  return verifyInvariantsImpl();
}

void aarch64_sme_ld1b_vert::getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
  for (::mlir::Value value : getODSOperands(1))
    effects.emplace_back(::mlir::MemoryEffects::Read::get(), value, ::mlir::SideEffects::DefaultResource::get());
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_ld1b_vert)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_ld1d_horiz definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_ld1d_horizGenericAdaptorBase::aarch64_sme_ld1d_horizGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.ld1d.horiz", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_ld1d_horizGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_ld1d_horizGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_ld1d_horizAdaptor::aarch64_sme_ld1d_horizAdaptor(aarch64_sme_ld1d_horiz op) : aarch64_sme_ld1d_horizAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_ld1d_horizAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_ld1d_horiz::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_ld1d_horiz::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_ld1d_horiz::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_ld1d_horiz::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_ld1d_horiz::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
}

void aarch64_sme_ld1d_horiz::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_ld1d_horiz::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 4u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_ld1d_horiz::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME1(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_ld1d_horiz::verifyInvariants() {
  return verifyInvariantsImpl();
}

void aarch64_sme_ld1d_horiz::getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
  for (::mlir::Value value : getODSOperands(1))
    effects.emplace_back(::mlir::MemoryEffects::Read::get(), value, ::mlir::SideEffects::DefaultResource::get());
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_ld1d_horiz)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_ld1d_vert definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_ld1d_vertGenericAdaptorBase::aarch64_sme_ld1d_vertGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.ld1d.vert", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_ld1d_vertGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_ld1d_vertGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_ld1d_vertAdaptor::aarch64_sme_ld1d_vertAdaptor(aarch64_sme_ld1d_vert op) : aarch64_sme_ld1d_vertAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_ld1d_vertAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_ld1d_vert::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_ld1d_vert::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_ld1d_vert::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_ld1d_vert::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_ld1d_vert::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
}

void aarch64_sme_ld1d_vert::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_ld1d_vert::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 4u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_ld1d_vert::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME1(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_ld1d_vert::verifyInvariants() {
  return verifyInvariantsImpl();
}

void aarch64_sme_ld1d_vert::getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
  for (::mlir::Value value : getODSOperands(1))
    effects.emplace_back(::mlir::MemoryEffects::Read::get(), value, ::mlir::SideEffects::DefaultResource::get());
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_ld1d_vert)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_ld1h_horiz definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_ld1h_horizGenericAdaptorBase::aarch64_sme_ld1h_horizGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.ld1h.horiz", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_ld1h_horizGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_ld1h_horizGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_ld1h_horizAdaptor::aarch64_sme_ld1h_horizAdaptor(aarch64_sme_ld1h_horiz op) : aarch64_sme_ld1h_horizAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_ld1h_horizAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_ld1h_horiz::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_ld1h_horiz::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_ld1h_horiz::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_ld1h_horiz::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_ld1h_horiz::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
}

void aarch64_sme_ld1h_horiz::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_ld1h_horiz::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 4u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_ld1h_horiz::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME1(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_ld1h_horiz::verifyInvariants() {
  return verifyInvariantsImpl();
}

void aarch64_sme_ld1h_horiz::getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
  for (::mlir::Value value : getODSOperands(1))
    effects.emplace_back(::mlir::MemoryEffects::Read::get(), value, ::mlir::SideEffects::DefaultResource::get());
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_ld1h_horiz)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_ld1h_vert definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_ld1h_vertGenericAdaptorBase::aarch64_sme_ld1h_vertGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.ld1h.vert", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_ld1h_vertGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_ld1h_vertGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_ld1h_vertAdaptor::aarch64_sme_ld1h_vertAdaptor(aarch64_sme_ld1h_vert op) : aarch64_sme_ld1h_vertAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_ld1h_vertAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_ld1h_vert::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_ld1h_vert::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_ld1h_vert::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_ld1h_vert::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_ld1h_vert::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
}

void aarch64_sme_ld1h_vert::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_ld1h_vert::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 4u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_ld1h_vert::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME1(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_ld1h_vert::verifyInvariants() {
  return verifyInvariantsImpl();
}

void aarch64_sme_ld1h_vert::getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
  for (::mlir::Value value : getODSOperands(1))
    effects.emplace_back(::mlir::MemoryEffects::Read::get(), value, ::mlir::SideEffects::DefaultResource::get());
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_ld1h_vert)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_ld1q_horiz definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_ld1q_horizGenericAdaptorBase::aarch64_sme_ld1q_horizGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.ld1q.horiz", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_ld1q_horizGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_ld1q_horizGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_ld1q_horizAdaptor::aarch64_sme_ld1q_horizAdaptor(aarch64_sme_ld1q_horiz op) : aarch64_sme_ld1q_horizAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_ld1q_horizAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_ld1q_horiz::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_ld1q_horiz::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_ld1q_horiz::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_ld1q_horiz::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_ld1q_horiz::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
}

void aarch64_sme_ld1q_horiz::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_ld1q_horiz::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 4u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_ld1q_horiz::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME1(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_ld1q_horiz::verifyInvariants() {
  return verifyInvariantsImpl();
}

void aarch64_sme_ld1q_horiz::getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
  for (::mlir::Value value : getODSOperands(1))
    effects.emplace_back(::mlir::MemoryEffects::Read::get(), value, ::mlir::SideEffects::DefaultResource::get());
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_ld1q_horiz)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_ld1q_vert definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_ld1q_vertGenericAdaptorBase::aarch64_sme_ld1q_vertGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.ld1q.vert", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_ld1q_vertGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_ld1q_vertGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_ld1q_vertAdaptor::aarch64_sme_ld1q_vertAdaptor(aarch64_sme_ld1q_vert op) : aarch64_sme_ld1q_vertAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_ld1q_vertAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_ld1q_vert::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_ld1q_vert::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_ld1q_vert::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_ld1q_vert::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_ld1q_vert::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
}

void aarch64_sme_ld1q_vert::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_ld1q_vert::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 4u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_ld1q_vert::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME1(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_ld1q_vert::verifyInvariants() {
  return verifyInvariantsImpl();
}

void aarch64_sme_ld1q_vert::getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
  for (::mlir::Value value : getODSOperands(1))
    effects.emplace_back(::mlir::MemoryEffects::Read::get(), value, ::mlir::SideEffects::DefaultResource::get());
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_ld1q_vert)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_ld1w_horiz definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_ld1w_horizGenericAdaptorBase::aarch64_sme_ld1w_horizGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.ld1w.horiz", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_ld1w_horizGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_ld1w_horizGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_ld1w_horizAdaptor::aarch64_sme_ld1w_horizAdaptor(aarch64_sme_ld1w_horiz op) : aarch64_sme_ld1w_horizAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_ld1w_horizAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_ld1w_horiz::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_ld1w_horiz::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_ld1w_horiz::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_ld1w_horiz::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_ld1w_horiz::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
}

void aarch64_sme_ld1w_horiz::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_ld1w_horiz::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 4u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_ld1w_horiz::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME1(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_ld1w_horiz::verifyInvariants() {
  return verifyInvariantsImpl();
}

void aarch64_sme_ld1w_horiz::getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
  for (::mlir::Value value : getODSOperands(1))
    effects.emplace_back(::mlir::MemoryEffects::Read::get(), value, ::mlir::SideEffects::DefaultResource::get());
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_ld1w_horiz)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_ld1w_vert definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_ld1w_vertGenericAdaptorBase::aarch64_sme_ld1w_vertGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.ld1w.vert", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_ld1w_vertGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_ld1w_vertGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_ld1w_vertAdaptor::aarch64_sme_ld1w_vertAdaptor(aarch64_sme_ld1w_vert op) : aarch64_sme_ld1w_vertAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_ld1w_vertAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_ld1w_vert::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_ld1w_vert::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_ld1w_vert::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_ld1w_vert::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_ld1w_vert::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
}

void aarch64_sme_ld1w_vert::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_ld1w_vert::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 4u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_ld1w_vert::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME1(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_ld1w_vert::verifyInvariants() {
  return verifyInvariantsImpl();
}

void aarch64_sme_ld1w_vert::getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
  for (::mlir::Value value : getODSOperands(1))
    effects.emplace_back(::mlir::MemoryEffects::Read::get(), value, ::mlir::SideEffects::DefaultResource::get());
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_ld1w_vert)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_mopa definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_mopaGenericAdaptorBase::aarch64_sme_mopaGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.mopa", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_mopaGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_mopaGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_mopaAdaptor::aarch64_sme_mopaAdaptor(aarch64_sme_mopa op) : aarch64_sme_mopaAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_mopaAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_mopa::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_mopa::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_mopa::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_mopa::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_mopa::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3, ::mlir::Value odsArg_4) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  odsState.addOperands(odsArg_4);
}

void aarch64_sme_mopa::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3, ::mlir::Value odsArg_4) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  odsState.addOperands(odsArg_4);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_mopa::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 5u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_mopa::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME3(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME3(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME4(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup4 = getODSOperands(4);

    for (auto v : valueGroup4) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME4(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_mopa::verifyInvariants() {
  return verifyInvariantsImpl();
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_mopa)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_mopa_wide definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_mopa_wideGenericAdaptorBase::aarch64_sme_mopa_wideGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.mopa.wide", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_mopa_wideGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_mopa_wideGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_mopa_wideAdaptor::aarch64_sme_mopa_wideAdaptor(aarch64_sme_mopa_wide op) : aarch64_sme_mopa_wideAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_mopa_wideAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_mopa_wide::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_mopa_wide::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_mopa_wide::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_mopa_wide::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_mopa_wide::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3, ::mlir::Value odsArg_4) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  odsState.addOperands(odsArg_4);
}

void aarch64_sme_mopa_wide::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3, ::mlir::Value odsArg_4) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  odsState.addOperands(odsArg_4);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_mopa_wide::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 5u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_mopa_wide::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME3(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME3(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME4(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup4 = getODSOperands(4);

    for (auto v : valueGroup4) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME4(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_mopa_wide::verifyInvariants() {
  return verifyInvariantsImpl();
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_mopa_wide)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_mops definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_mopsGenericAdaptorBase::aarch64_sme_mopsGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.mops", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_mopsGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_mopsGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_mopsAdaptor::aarch64_sme_mopsAdaptor(aarch64_sme_mops op) : aarch64_sme_mopsAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_mopsAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_mops::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_mops::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_mops::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_mops::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_mops::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3, ::mlir::Value odsArg_4) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  odsState.addOperands(odsArg_4);
}

void aarch64_sme_mops::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3, ::mlir::Value odsArg_4) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  odsState.addOperands(odsArg_4);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_mops::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 5u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_mops::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME3(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME3(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME4(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup4 = getODSOperands(4);

    for (auto v : valueGroup4) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME4(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_mops::verifyInvariants() {
  return verifyInvariantsImpl();
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_mops)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_mops_wide definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_mops_wideGenericAdaptorBase::aarch64_sme_mops_wideGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.mops.wide", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_mops_wideGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_mops_wideGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_mops_wideAdaptor::aarch64_sme_mops_wideAdaptor(aarch64_sme_mops_wide op) : aarch64_sme_mops_wideAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_mops_wideAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_mops_wide::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_mops_wide::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_mops_wide::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_mops_wide::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_mops_wide::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3, ::mlir::Value odsArg_4) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  odsState.addOperands(odsArg_4);
}

void aarch64_sme_mops_wide::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3, ::mlir::Value odsArg_4) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  odsState.addOperands(odsArg_4);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_mops_wide::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 5u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_mops_wide::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME3(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME3(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME4(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup4 = getODSOperands(4);

    for (auto v : valueGroup4) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME4(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_mops_wide::verifyInvariants() {
  return verifyInvariantsImpl();
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_mops_wide)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_smopa_wide definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_smopa_wideGenericAdaptorBase::aarch64_sme_smopa_wideGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.smopa.wide", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_smopa_wideGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_smopa_wideGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_smopa_wideAdaptor::aarch64_sme_smopa_wideAdaptor(aarch64_sme_smopa_wide op) : aarch64_sme_smopa_wideAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_smopa_wideAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_smopa_wide::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_smopa_wide::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_smopa_wide::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_smopa_wide::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_smopa_wide::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3, ::mlir::Value odsArg_4) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  odsState.addOperands(odsArg_4);
}

void aarch64_sme_smopa_wide::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3, ::mlir::Value odsArg_4) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  odsState.addOperands(odsArg_4);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_smopa_wide::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 5u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_smopa_wide::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME3(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME3(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME4(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup4 = getODSOperands(4);

    for (auto v : valueGroup4) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME4(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_smopa_wide::verifyInvariants() {
  return verifyInvariantsImpl();
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_smopa_wide)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_smops_wide definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_smops_wideGenericAdaptorBase::aarch64_sme_smops_wideGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.smops.wide", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_smops_wideGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_smops_wideGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_smops_wideAdaptor::aarch64_sme_smops_wideAdaptor(aarch64_sme_smops_wide op) : aarch64_sme_smops_wideAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_smops_wideAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_smops_wide::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_smops_wide::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_smops_wide::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_smops_wide::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_smops_wide::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3, ::mlir::Value odsArg_4) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  odsState.addOperands(odsArg_4);
}

void aarch64_sme_smops_wide::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3, ::mlir::Value odsArg_4) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  odsState.addOperands(odsArg_4);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_smops_wide::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 5u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_smops_wide::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME3(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME3(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME4(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup4 = getODSOperands(4);

    for (auto v : valueGroup4) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME4(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_smops_wide::verifyInvariants() {
  return verifyInvariantsImpl();
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_smops_wide)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_st1b_horiz definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_st1b_horizGenericAdaptorBase::aarch64_sme_st1b_horizGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.st1b.horiz", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_st1b_horizGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_st1b_horizGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_st1b_horizAdaptor::aarch64_sme_st1b_horizAdaptor(aarch64_sme_st1b_horiz op) : aarch64_sme_st1b_horizAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_st1b_horizAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_st1b_horiz::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_st1b_horiz::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_st1b_horiz::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_st1b_horiz::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_st1b_horiz::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
}

void aarch64_sme_st1b_horiz::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_st1b_horiz::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 4u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_st1b_horiz::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME1(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_st1b_horiz::verifyInvariants() {
  return verifyInvariantsImpl();
}

void aarch64_sme_st1b_horiz::getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
  for (::mlir::Value value : getODSOperands(1))
    effects.emplace_back(::mlir::MemoryEffects::Write::get(), value, ::mlir::SideEffects::DefaultResource::get());
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_st1b_horiz)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_st1b_vert definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_st1b_vertGenericAdaptorBase::aarch64_sme_st1b_vertGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.st1b.vert", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_st1b_vertGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_st1b_vertGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_st1b_vertAdaptor::aarch64_sme_st1b_vertAdaptor(aarch64_sme_st1b_vert op) : aarch64_sme_st1b_vertAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_st1b_vertAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_st1b_vert::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_st1b_vert::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_st1b_vert::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_st1b_vert::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_st1b_vert::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
}

void aarch64_sme_st1b_vert::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_st1b_vert::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 4u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_st1b_vert::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME1(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_st1b_vert::verifyInvariants() {
  return verifyInvariantsImpl();
}

void aarch64_sme_st1b_vert::getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
  for (::mlir::Value value : getODSOperands(1))
    effects.emplace_back(::mlir::MemoryEffects::Write::get(), value, ::mlir::SideEffects::DefaultResource::get());
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_st1b_vert)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_st1d_horiz definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_st1d_horizGenericAdaptorBase::aarch64_sme_st1d_horizGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.st1d.horiz", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_st1d_horizGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_st1d_horizGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_st1d_horizAdaptor::aarch64_sme_st1d_horizAdaptor(aarch64_sme_st1d_horiz op) : aarch64_sme_st1d_horizAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_st1d_horizAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_st1d_horiz::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_st1d_horiz::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_st1d_horiz::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_st1d_horiz::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_st1d_horiz::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
}

void aarch64_sme_st1d_horiz::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_st1d_horiz::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 4u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_st1d_horiz::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME1(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_st1d_horiz::verifyInvariants() {
  return verifyInvariantsImpl();
}

void aarch64_sme_st1d_horiz::getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
  for (::mlir::Value value : getODSOperands(1))
    effects.emplace_back(::mlir::MemoryEffects::Write::get(), value, ::mlir::SideEffects::DefaultResource::get());
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_st1d_horiz)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_st1d_vert definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_st1d_vertGenericAdaptorBase::aarch64_sme_st1d_vertGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.st1d.vert", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_st1d_vertGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_st1d_vertGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_st1d_vertAdaptor::aarch64_sme_st1d_vertAdaptor(aarch64_sme_st1d_vert op) : aarch64_sme_st1d_vertAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_st1d_vertAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_st1d_vert::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_st1d_vert::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_st1d_vert::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_st1d_vert::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_st1d_vert::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
}

void aarch64_sme_st1d_vert::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_st1d_vert::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 4u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_st1d_vert::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME1(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_st1d_vert::verifyInvariants() {
  return verifyInvariantsImpl();
}

void aarch64_sme_st1d_vert::getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
  for (::mlir::Value value : getODSOperands(1))
    effects.emplace_back(::mlir::MemoryEffects::Write::get(), value, ::mlir::SideEffects::DefaultResource::get());
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_st1d_vert)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_st1h_horiz definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_st1h_horizGenericAdaptorBase::aarch64_sme_st1h_horizGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.st1h.horiz", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_st1h_horizGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_st1h_horizGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_st1h_horizAdaptor::aarch64_sme_st1h_horizAdaptor(aarch64_sme_st1h_horiz op) : aarch64_sme_st1h_horizAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_st1h_horizAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_st1h_horiz::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_st1h_horiz::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_st1h_horiz::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_st1h_horiz::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_st1h_horiz::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
}

void aarch64_sme_st1h_horiz::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_st1h_horiz::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 4u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_st1h_horiz::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME1(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_st1h_horiz::verifyInvariants() {
  return verifyInvariantsImpl();
}

void aarch64_sme_st1h_horiz::getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
  for (::mlir::Value value : getODSOperands(1))
    effects.emplace_back(::mlir::MemoryEffects::Write::get(), value, ::mlir::SideEffects::DefaultResource::get());
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_st1h_horiz)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_st1h_vert definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_st1h_vertGenericAdaptorBase::aarch64_sme_st1h_vertGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.st1h.vert", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_st1h_vertGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_st1h_vertGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_st1h_vertAdaptor::aarch64_sme_st1h_vertAdaptor(aarch64_sme_st1h_vert op) : aarch64_sme_st1h_vertAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_st1h_vertAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_st1h_vert::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_st1h_vert::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_st1h_vert::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_st1h_vert::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_st1h_vert::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
}

void aarch64_sme_st1h_vert::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_st1h_vert::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 4u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_st1h_vert::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME1(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_st1h_vert::verifyInvariants() {
  return verifyInvariantsImpl();
}

void aarch64_sme_st1h_vert::getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
  for (::mlir::Value value : getODSOperands(1))
    effects.emplace_back(::mlir::MemoryEffects::Write::get(), value, ::mlir::SideEffects::DefaultResource::get());
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_st1h_vert)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_st1q_horiz definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_st1q_horizGenericAdaptorBase::aarch64_sme_st1q_horizGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.st1q.horiz", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_st1q_horizGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_st1q_horizGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_st1q_horizAdaptor::aarch64_sme_st1q_horizAdaptor(aarch64_sme_st1q_horiz op) : aarch64_sme_st1q_horizAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_st1q_horizAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_st1q_horiz::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_st1q_horiz::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_st1q_horiz::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_st1q_horiz::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_st1q_horiz::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
}

void aarch64_sme_st1q_horiz::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_st1q_horiz::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 4u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_st1q_horiz::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME1(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_st1q_horiz::verifyInvariants() {
  return verifyInvariantsImpl();
}

void aarch64_sme_st1q_horiz::getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
  for (::mlir::Value value : getODSOperands(1))
    effects.emplace_back(::mlir::MemoryEffects::Write::get(), value, ::mlir::SideEffects::DefaultResource::get());
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_st1q_horiz)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_st1q_vert definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_st1q_vertGenericAdaptorBase::aarch64_sme_st1q_vertGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.st1q.vert", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_st1q_vertGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_st1q_vertGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_st1q_vertAdaptor::aarch64_sme_st1q_vertAdaptor(aarch64_sme_st1q_vert op) : aarch64_sme_st1q_vertAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_st1q_vertAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_st1q_vert::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_st1q_vert::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_st1q_vert::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_st1q_vert::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_st1q_vert::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
}

void aarch64_sme_st1q_vert::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_st1q_vert::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 4u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_st1q_vert::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME1(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_st1q_vert::verifyInvariants() {
  return verifyInvariantsImpl();
}

void aarch64_sme_st1q_vert::getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
  for (::mlir::Value value : getODSOperands(1))
    effects.emplace_back(::mlir::MemoryEffects::Write::get(), value, ::mlir::SideEffects::DefaultResource::get());
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_st1q_vert)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_st1w_horiz definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_st1w_horizGenericAdaptorBase::aarch64_sme_st1w_horizGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.st1w.horiz", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_st1w_horizGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_st1w_horizGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_st1w_horizAdaptor::aarch64_sme_st1w_horizAdaptor(aarch64_sme_st1w_horiz op) : aarch64_sme_st1w_horizAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_st1w_horizAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_st1w_horiz::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_st1w_horiz::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_st1w_horiz::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_st1w_horiz::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_st1w_horiz::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
}

void aarch64_sme_st1w_horiz::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_st1w_horiz::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 4u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_st1w_horiz::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME1(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_st1w_horiz::verifyInvariants() {
  return verifyInvariantsImpl();
}

void aarch64_sme_st1w_horiz::getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
  for (::mlir::Value value : getODSOperands(1))
    effects.emplace_back(::mlir::MemoryEffects::Write::get(), value, ::mlir::SideEffects::DefaultResource::get());
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_st1w_horiz)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_st1w_vert definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_st1w_vertGenericAdaptorBase::aarch64_sme_st1w_vertGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.st1w.vert", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_st1w_vertGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_st1w_vertGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_st1w_vertAdaptor::aarch64_sme_st1w_vertAdaptor(aarch64_sme_st1w_vert op) : aarch64_sme_st1w_vertAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_st1w_vertAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_st1w_vert::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_st1w_vert::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_st1w_vert::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_st1w_vert::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_st1w_vert::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
}

void aarch64_sme_st1w_vert::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_st1w_vert::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 4u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_st1w_vert::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME0(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME1(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_st1w_vert::verifyInvariants() {
  return verifyInvariantsImpl();
}

void aarch64_sme_st1w_vert::getEffects(::llvm::SmallVectorImpl<::mlir::SideEffects::EffectInstance<::mlir::MemoryEffects::Effect>> &effects) {
  for (::mlir::Value value : getODSOperands(1))
    effects.emplace_back(::mlir::MemoryEffects::Write::get(), value, ::mlir::SideEffects::DefaultResource::get());
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_st1w_vert)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_sumopa_wide definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_sumopa_wideGenericAdaptorBase::aarch64_sme_sumopa_wideGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.sumopa.wide", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_sumopa_wideGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_sumopa_wideGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_sumopa_wideAdaptor::aarch64_sme_sumopa_wideAdaptor(aarch64_sme_sumopa_wide op) : aarch64_sme_sumopa_wideAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_sumopa_wideAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_sumopa_wide::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_sumopa_wide::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_sumopa_wide::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_sumopa_wide::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_sumopa_wide::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3, ::mlir::Value odsArg_4) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  odsState.addOperands(odsArg_4);
}

void aarch64_sme_sumopa_wide::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3, ::mlir::Value odsArg_4) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  odsState.addOperands(odsArg_4);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_sumopa_wide::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 5u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_sumopa_wide::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME3(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME3(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME4(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup4 = getODSOperands(4);

    for (auto v : valueGroup4) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME4(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_sumopa_wide::verifyInvariants() {
  return verifyInvariantsImpl();
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_sumopa_wide)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_sumops_wide definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_sumops_wideGenericAdaptorBase::aarch64_sme_sumops_wideGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.sumops.wide", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_sumops_wideGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_sumops_wideGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_sumops_wideAdaptor::aarch64_sme_sumops_wideAdaptor(aarch64_sme_sumops_wide op) : aarch64_sme_sumops_wideAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_sumops_wideAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_sumops_wide::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_sumops_wide::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_sumops_wide::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_sumops_wide::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_sumops_wide::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3, ::mlir::Value odsArg_4) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  odsState.addOperands(odsArg_4);
}

void aarch64_sme_sumops_wide::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3, ::mlir::Value odsArg_4) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  odsState.addOperands(odsArg_4);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_sumops_wide::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 5u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_sumops_wide::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME3(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME3(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME4(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup4 = getODSOperands(4);

    for (auto v : valueGroup4) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME4(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_sumops_wide::verifyInvariants() {
  return verifyInvariantsImpl();
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_sumops_wide)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_umopa_wide definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_umopa_wideGenericAdaptorBase::aarch64_sme_umopa_wideGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.umopa.wide", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_umopa_wideGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_umopa_wideGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_umopa_wideAdaptor::aarch64_sme_umopa_wideAdaptor(aarch64_sme_umopa_wide op) : aarch64_sme_umopa_wideAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_umopa_wideAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_umopa_wide::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_umopa_wide::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_umopa_wide::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_umopa_wide::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_umopa_wide::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3, ::mlir::Value odsArg_4) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  odsState.addOperands(odsArg_4);
}

void aarch64_sme_umopa_wide::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3, ::mlir::Value odsArg_4) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  odsState.addOperands(odsArg_4);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_umopa_wide::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 5u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_umopa_wide::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME3(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME3(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME4(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup4 = getODSOperands(4);

    for (auto v : valueGroup4) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME4(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_umopa_wide::verifyInvariants() {
  return verifyInvariantsImpl();
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_umopa_wide)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_umops_wide definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_umops_wideGenericAdaptorBase::aarch64_sme_umops_wideGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.umops.wide", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_umops_wideGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_umops_wideGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_umops_wideAdaptor::aarch64_sme_umops_wideAdaptor(aarch64_sme_umops_wide op) : aarch64_sme_umops_wideAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_umops_wideAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_umops_wide::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_umops_wide::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_umops_wide::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_umops_wide::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_umops_wide::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3, ::mlir::Value odsArg_4) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  odsState.addOperands(odsArg_4);
}

void aarch64_sme_umops_wide::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3, ::mlir::Value odsArg_4) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  odsState.addOperands(odsArg_4);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_umops_wide::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 5u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_umops_wide::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME3(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME3(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME4(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup4 = getODSOperands(4);

    for (auto v : valueGroup4) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME4(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_umops_wide::verifyInvariants() {
  return verifyInvariantsImpl();
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_umops_wide)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_usmopa_wide definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_usmopa_wideGenericAdaptorBase::aarch64_sme_usmopa_wideGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.usmopa.wide", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_usmopa_wideGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_usmopa_wideGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_usmopa_wideAdaptor::aarch64_sme_usmopa_wideAdaptor(aarch64_sme_usmopa_wide op) : aarch64_sme_usmopa_wideAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_usmopa_wideAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_usmopa_wide::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_usmopa_wide::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_usmopa_wide::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_usmopa_wide::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_usmopa_wide::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3, ::mlir::Value odsArg_4) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  odsState.addOperands(odsArg_4);
}

void aarch64_sme_usmopa_wide::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3, ::mlir::Value odsArg_4) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  odsState.addOperands(odsArg_4);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_usmopa_wide::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 5u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_usmopa_wide::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME3(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME3(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME4(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup4 = getODSOperands(4);

    for (auto v : valueGroup4) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME4(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_usmopa_wide::verifyInvariants() {
  return verifyInvariantsImpl();
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_usmopa_wide)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_usmops_wide definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_usmops_wideGenericAdaptorBase::aarch64_sme_usmops_wideGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.usmops.wide", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_usmops_wideGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_usmops_wideGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_usmops_wideAdaptor::aarch64_sme_usmops_wideAdaptor(aarch64_sme_usmops_wide op) : aarch64_sme_usmops_wideAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_usmops_wideAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_usmops_wide::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_usmops_wide::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_usmops_wide::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_usmops_wide::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_usmops_wide::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3, ::mlir::Value odsArg_4) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  odsState.addOperands(odsArg_4);
}

void aarch64_sme_usmops_wide::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0, ::mlir::Value odsArg_1, ::mlir::Value odsArg_2, ::mlir::Value odsArg_3, ::mlir::Value odsArg_4) {
  odsState.addOperands(odsArg_0);
  odsState.addOperands(odsArg_1);
  odsState.addOperands(odsArg_2);
  odsState.addOperands(odsArg_3);
  odsState.addOperands(odsArg_4);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_usmops_wide::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 5u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_usmops_wide::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup1 = getODSOperands(1);

    for (auto v : valueGroup1) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME3(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup2 = getODSOperands(2);

    for (auto v : valueGroup2) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME3(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup3 = getODSOperands(3);

    for (auto v : valueGroup3) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME4(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
    auto valueGroup4 = getODSOperands(4);

    for (auto v : valueGroup4) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME4(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_usmops_wide::verifyInvariants() {
  return verifyInvariantsImpl();
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_usmops_wide)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_za_disable definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_za_disableGenericAdaptorBase::aarch64_sme_za_disableGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.za.disable", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_za_disableGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_za_disableGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_za_disableAdaptor::aarch64_sme_za_disableAdaptor(aarch64_sme_za_disable op) : aarch64_sme_za_disableAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_za_disableAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_za_disable::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_za_disable::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_za_disable::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_za_disable::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_za_disable::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState) {
}

void aarch64_sme_za_disable::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes) {
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_za_disable::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 0u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_za_disable::verifyInvariantsImpl() {
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_za_disable::verifyInvariants() {
  return verifyInvariantsImpl();
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_za_disable)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_za_enable definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_za_enableGenericAdaptorBase::aarch64_sme_za_enableGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.za.enable", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_za_enableGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_za_enableGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_za_enableAdaptor::aarch64_sme_za_enableAdaptor(aarch64_sme_za_enable op) : aarch64_sme_za_enableAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_za_enableAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_za_enable::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_za_enable::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_za_enable::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_za_enable::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_za_enable::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState) {
}

void aarch64_sme_za_enable::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes) {
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_za_enable::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 0u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_za_enable::verifyInvariantsImpl() {
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_za_enable::verifyInvariants() {
  return verifyInvariantsImpl();
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_za_enable)

namespace mlir {
namespace arm_sme {

//===----------------------------------------------------------------------===//
// ::mlir::arm_sme::aarch64_sme_zero definitions
//===----------------------------------------------------------------------===//

namespace detail {
aarch64_sme_zeroGenericAdaptorBase::aarch64_sme_zeroGenericAdaptorBase(::mlir::DictionaryAttr attrs, const ::mlir::EmptyProperties &properties, ::mlir::RegionRange regions) : odsAttrs(attrs), odsRegions(regions) {  if (odsAttrs)
    odsOpName.emplace("arm_sme.intr.zero", odsAttrs.getContext());
}

std::pair<unsigned, unsigned> aarch64_sme_zeroGenericAdaptorBase::getODSOperandIndexAndLength(unsigned index, unsigned odsOperandsSize) {
  return {index, 1};
}

::mlir::DictionaryAttr aarch64_sme_zeroGenericAdaptorBase::getAttributes() {
  return odsAttrs;
}

} // namespace detail
aarch64_sme_zeroAdaptor::aarch64_sme_zeroAdaptor(aarch64_sme_zero op) : aarch64_sme_zeroAdaptor(op->getOperands(), op->getAttrDictionary(), op.getProperties(), op->getRegions()) {}

::mlir::LogicalResult aarch64_sme_zeroAdaptor::verify(::mlir::Location loc) {
  return ::mlir::success();
}

std::pair<unsigned, unsigned> aarch64_sme_zero::getODSOperandIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::operand_range aarch64_sme_zero::getODSOperands(unsigned index) {
  auto valueRange = getODSOperandIndexAndLength(index);
  return {std::next(getOperation()->operand_begin(), valueRange.first),
           std::next(getOperation()->operand_begin(), valueRange.first + valueRange.second)};
}

std::pair<unsigned, unsigned> aarch64_sme_zero::getODSResultIndexAndLength(unsigned index) {
  return {index, 1};
}

::mlir::Operation::result_range aarch64_sme_zero::getODSResults(unsigned index) {
  auto valueRange = getODSResultIndexAndLength(index);
  return {std::next(getOperation()->result_begin(), valueRange.first),
           std::next(getOperation()->result_begin(), valueRange.first + valueRange.second)};
}

void aarch64_sme_zero::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::Value odsArg_0) {
  odsState.addOperands(odsArg_0);
}

void aarch64_sme_zero::build(::mlir::OpBuilder &odsBuilder, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::Value odsArg_0) {
  odsState.addOperands(odsArg_0);
  assert(resultTypes.size() == 0u && "mismatched number of results");
  odsState.addTypes(resultTypes);
}

void aarch64_sme_zero::build(::mlir::OpBuilder &, ::mlir::OperationState &odsState, ::mlir::TypeRange resultTypes, ::mlir::ValueRange operands, ::llvm::ArrayRef<::mlir::NamedAttribute> attributes) {
  assert(operands.size() == 1u && "mismatched number of parameters");
  odsState.addOperands(operands);
  odsState.addAttributes(attributes);
  assert(resultTypes.size() == 0u && "mismatched number of return types");
  odsState.addTypes(resultTypes);
}

::mlir::LogicalResult aarch64_sme_zero::verifyInvariantsImpl() {
  {
    unsigned index = 0; (void)index;
    auto valueGroup0 = getODSOperands(0);

    for (auto v : valueGroup0) {
      if (::mlir::failed(__mlir_ods_local_type_constraint_ArmSME2(*this, v.getType(), "operand", index++)))
        return ::mlir::failure();
    }
  }
  return ::mlir::success();
}

::mlir::LogicalResult aarch64_sme_zero::verifyInvariants() {
  return verifyInvariantsImpl();
}

} // namespace arm_sme
} // namespace mlir
MLIR_DEFINE_EXPLICIT_TYPE_ID(::mlir::arm_sme::aarch64_sme_zero)


#endif  // GET_OP_CLASSES

