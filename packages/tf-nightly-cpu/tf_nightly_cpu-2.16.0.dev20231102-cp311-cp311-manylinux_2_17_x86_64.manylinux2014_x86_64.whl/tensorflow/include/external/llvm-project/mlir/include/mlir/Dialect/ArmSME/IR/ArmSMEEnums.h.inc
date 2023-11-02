/*===- TableGen'erated file -------------------------------------*- C++ -*-===*\
|*                                                                            *|
|* Enum Utility Declarations                                                  *|
|*                                                                            *|
|* Automatically generated file, do not edit!                                 *|
|* From: ArmSMEOps.td                                                         *|
|*                                                                            *|
\*===----------------------------------------------------------------------===*/

namespace mlir {
namespace arm_sme {
// Kind of combining function
enum class CombiningKind : uint32_t {
  Add = 0,
  Sub = 1,
};

::std::optional<CombiningKind> symbolizeCombiningKind(uint32_t);
::llvm::StringRef stringifyCombiningKind(CombiningKind);
::std::optional<CombiningKind> symbolizeCombiningKind(::llvm::StringRef);
inline constexpr unsigned getMaxEnumValForCombiningKind() {
  return 1;
}


inline ::llvm::StringRef stringifyEnum(CombiningKind enumValue) {
  return stringifyCombiningKind(enumValue);
}

template <typename EnumType>
::std::optional<EnumType> symbolizeEnum(::llvm::StringRef);

template <>
inline ::std::optional<CombiningKind> symbolizeEnum<CombiningKind>(::llvm::StringRef str) {
  return symbolizeCombiningKind(str);
}
} // namespace arm_sme
} // namespace mlir

namespace mlir {
template <typename T, typename>
struct FieldParser;

template<>
struct FieldParser<::mlir::arm_sme::CombiningKind, ::mlir::arm_sme::CombiningKind> {
  template <typename ParserT>
  static FailureOr<::mlir::arm_sme::CombiningKind> parse(ParserT &parser) {
    // Parse the keyword/string containing the enum.
    std::string enumKeyword;
    auto loc = parser.getCurrentLocation();
    if (failed(parser.parseOptionalKeywordOrString(&enumKeyword)))
      return parser.emitError(loc, "expected keyword for Kind of combining function");

    // Symbolize the keyword.
    if (::std::optional<::mlir::arm_sme::CombiningKind> attr = ::mlir::arm_sme::symbolizeEnum<::mlir::arm_sme::CombiningKind>(enumKeyword))
      return *attr;
    return parser.emitError(loc, "invalid Kind of combining function specification: ") << enumKeyword;
  }
};
} // namespace mlir

namespace llvm {
inline ::llvm::raw_ostream &operator<<(::llvm::raw_ostream &p, ::mlir::arm_sme::CombiningKind value) {
  auto valueStr = stringifyEnum(value);
  return p << valueStr;
}
} // namespace llvm

namespace llvm {
template<> struct DenseMapInfo<::mlir::arm_sme::CombiningKind> {
  using StorageInfo = ::llvm::DenseMapInfo<uint32_t>;

  static inline ::mlir::arm_sme::CombiningKind getEmptyKey() {
    return static_cast<::mlir::arm_sme::CombiningKind>(StorageInfo::getEmptyKey());
  }

  static inline ::mlir::arm_sme::CombiningKind getTombstoneKey() {
    return static_cast<::mlir::arm_sme::CombiningKind>(StorageInfo::getTombstoneKey());
  }

  static unsigned getHashValue(const ::mlir::arm_sme::CombiningKind &val) {
    return StorageInfo::getHashValue(static_cast<uint32_t>(val));
  }

  static bool isEqual(const ::mlir::arm_sme::CombiningKind &lhs, const ::mlir::arm_sme::CombiningKind &rhs) {
    return lhs == rhs;
  }
};
}

namespace mlir {
namespace arm_sme {
// Layout of a tile slice
enum class TileSliceLayout : uint32_t {
  Horizontal = 0,
  Vertical = 1,
};

::std::optional<TileSliceLayout> symbolizeTileSliceLayout(uint32_t);
::llvm::StringRef stringifyTileSliceLayout(TileSliceLayout);
::std::optional<TileSliceLayout> symbolizeTileSliceLayout(::llvm::StringRef);
inline constexpr unsigned getMaxEnumValForTileSliceLayout() {
  return 1;
}


inline ::llvm::StringRef stringifyEnum(TileSliceLayout enumValue) {
  return stringifyTileSliceLayout(enumValue);
}

template <typename EnumType>
::std::optional<EnumType> symbolizeEnum(::llvm::StringRef);

template <>
inline ::std::optional<TileSliceLayout> symbolizeEnum<TileSliceLayout>(::llvm::StringRef str) {
  return symbolizeTileSliceLayout(str);
}
} // namespace arm_sme
} // namespace mlir

namespace mlir {
template <typename T, typename>
struct FieldParser;

template<>
struct FieldParser<::mlir::arm_sme::TileSliceLayout, ::mlir::arm_sme::TileSliceLayout> {
  template <typename ParserT>
  static FailureOr<::mlir::arm_sme::TileSliceLayout> parse(ParserT &parser) {
    // Parse the keyword/string containing the enum.
    std::string enumKeyword;
    auto loc = parser.getCurrentLocation();
    if (failed(parser.parseOptionalKeywordOrString(&enumKeyword)))
      return parser.emitError(loc, "expected keyword for Layout of a tile slice");

    // Symbolize the keyword.
    if (::std::optional<::mlir::arm_sme::TileSliceLayout> attr = ::mlir::arm_sme::symbolizeEnum<::mlir::arm_sme::TileSliceLayout>(enumKeyword))
      return *attr;
    return parser.emitError(loc, "invalid Layout of a tile slice specification: ") << enumKeyword;
  }
};
} // namespace mlir

namespace llvm {
inline ::llvm::raw_ostream &operator<<(::llvm::raw_ostream &p, ::mlir::arm_sme::TileSliceLayout value) {
  auto valueStr = stringifyEnum(value);
  return p << valueStr;
}
} // namespace llvm

namespace llvm {
template<> struct DenseMapInfo<::mlir::arm_sme::TileSliceLayout> {
  using StorageInfo = ::llvm::DenseMapInfo<uint32_t>;

  static inline ::mlir::arm_sme::TileSliceLayout getEmptyKey() {
    return static_cast<::mlir::arm_sme::TileSliceLayout>(StorageInfo::getEmptyKey());
  }

  static inline ::mlir::arm_sme::TileSliceLayout getTombstoneKey() {
    return static_cast<::mlir::arm_sme::TileSliceLayout>(StorageInfo::getTombstoneKey());
  }

  static unsigned getHashValue(const ::mlir::arm_sme::TileSliceLayout &val) {
    return StorageInfo::getHashValue(static_cast<uint32_t>(val));
  }

  static bool isEqual(const ::mlir::arm_sme::TileSliceLayout &lhs, const ::mlir::arm_sme::TileSliceLayout &rhs) {
    return lhs == rhs;
  }
};
}

