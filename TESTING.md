# CrossPacket Testing Guide

This document describes how CrossPacket is tested across all 9 supported programming languages.

## Overview

CrossPacket uses a comprehensive testing strategy to ensure:

- **100% code coverage** across all generated packet code
- **Cross-language compatibility** - packets serialize/deserialize correctly in all languages
- **Robust error handling** - edge cases and corrupt data are handled gracefully
- **CI/CD integration** - automated testing via GitHub Actions with coverage reporting to Codecov

## Test Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      GitHub Actions                             │
├─────────────────────────────────────────────────────────────────┤
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │ CI Workflow │  │  Generate   │  │  Coverage   │              │
│  │  (ci.yml)   │──│  Workflow   │──│  Workflow   │              │
│  │             │  │             │  │             │              │
│  │ Quick tests │  │ Regenerate  │  │ Full tests  │              │
│  │ all langs   │  │ all code    │  │ + coverage  │              │
│  └─────────────┘  └─────────────┘  └─────────────┘              │
│                                            │                    │
│                                            ▼                    │
│                                    ┌─────────────┐              │
│                                    │   Codecov   │              │
│                                    │  Dashboard  │              │
│                                    └─────────────┘              │
└─────────────────────────────────────────────────────────────────┘
```

## Coverage Workflow

The coverage workflow (`coverage.yml`) runs after the Generate Code workflow completes:

1. **Checks for bot commit** - Only runs on commits made by the code generator bot
2. **Tests all 9 languages** in parallel:
   - TypeScript, Python, Go, Java, C#, Dart, PHP, Rust, C++
3. **Uploads to Codecov** - Each language uploads its coverage report with a unique flag

## Test Suites by Language

### TypeScript (`tests/typescript/`)

**Framework:** Jest  
**Coverage Tool:** Jest built-in coverage

```bash
cd tests/typescript
npm install
npx jest --coverage
```

**Test File:** `packets.test.ts`

- Tests all 7 packet types
- JSON and MsgPack serialization roundtrips
- Edge cases: empty strings, large numbers, unicode, binary data
- Error handling: malformed JSON, corrupt MsgPack

### Python (`tests/python/`)

**Framework:** pytest  
**Coverage Tool:** pytest-cov

```bash
pip install pytest pytest-cov msgpack
python -m pytest tests/python/ -v --cov=generated/python --cov-report=html
```

**Test Files:**

- `test_generated_packets.py` - Main packet tests
- `test_security_utils.py` - Security utilities

Features:

- Parametrized tests for all packet types
- Datetime handling across timezones
- Optional field handling (None values)
- Corrupt data simulation

### Go (`generated/go/`)

**Framework:** Go testing  
**Coverage Tool:** go test -coverprofile

```bash
cd generated/go
go mod init crosspacket/packets
go mod tidy
go test -coverprofile=coverage.out -covermode=atomic ./...
```

Tests are generated inline in the coverage workflow to ensure they use the correct API:

- Factory function pattern: `PingPacketFromJSON(data)` not `p.FromJSON(data)`
- Pointer types for optional fields: `*string`, `*int64`

### Java (`tests/java/`)

**Framework:** JUnit 5  
**Coverage Tool:** JaCoCo

```bash
cd tests/java
mvn test jacoco:report
```

**Test Class:** `PacketTest.java`

- Tests all packet types with builder patterns
- JSON/MsgPack roundtrip tests
- Getter/setter coverage
- Null safety tests

### C# (`tests/csharp/`)

**Framework:** xUnit  
**Coverage Tool:** XPlat Code Coverage (Coverlet)

```bash
cd tests/csharp
dotnet test --collect:"XPlat Code Coverage"
```

**Test File:** `PacketTests.cs`

- All packet types tested
- Nullable reference type handling
- Binary data serialization
- Edge cases with special characters

### Dart (`tests/dart/`)

**Framework:** dart test  
**Coverage Tool:** dart coverage

```bash
cd tests/dart
dart pub get
dart test --coverage=coverage
dart pub global run coverage:format_coverage --lcov --in=coverage --out=coverage/lcov.info
```

**Test File:** `test/packets_test.dart`

- Static factory method tests (`fromJson`, `fromMsgPack`)
- Full roundtrip serialization
- Null-safety validation
- Type coercion tests

### PHP (`tests/php/`)

**Framework:** PHPUnit 10  
**Coverage Tool:** PHPUnit + Xdebug

```bash
cd tests/php
composer install
php vendor/bin/phpunit --coverage-clover coverage.xml
```

**Test File:** `PacketTest.php`

- PSR-4 autoloading from generated/php/
- Type-safe tests with strict typing
- Binary data handling with base64
- Error handling for invalid data

### Rust (`tests/rust/`)

**Framework:** Rust test  
**Coverage Tool:** cargo-tarpaulin

```bash
cd tests/rust
cargo tarpaulin --out Xml
```

**Test File:** `tests/packets_test.rs`

- Uses `crosspacket_generated` crate from `generated/rust/`
- Owned vs borrowed type handling
- serde derive testing
- Chrono datetime serialization

### C++ (`tests/cpp/`)

**Framework:** Catch2 v3  
**Coverage Tool:** lcov/gcov

```bash
cd tests/cpp
g++ -std=c++17 -fprofile-arcs -ftest-coverage -I../../generated/cpp \
    test_catch2.cpp ../../generated/cpp/*.cpp \
    -lyyjson -lCatch2Main -lCatch2 -o test_catch2
./test_catch2
lcov --capture --directory . --output-file coverage.info
```

**Test File:** `test_catch2.cpp`

- Parameterized constructor tests
- `std::optional` field handling
- yyjson for JSON, msgpack-c for MsgPack
- Float comparison with epsilon tolerance

## Test Modes

CrossPacket supports three test modes based on what serialization formats are enabled:

| Mode           | JSON | MsgPack | Environment Variable     |
| -------------- | ---- | ------- | ------------------------ |
| `BOTH`         | ✅   | ✅      | `TEST_MODE=BOTH`         |
| `JSON_ONLY`    | ✅   | ❌      | `TEST_MODE=JSON_ONLY`    |
| `MSGPACK_ONLY` | ❌   | ✅      | `TEST_MODE=MSGPACK_ONLY` |

Tests automatically detect available methods and skip tests for unavailable features.

## Edge Cases Tested

All test suites cover these edge cases:

### Data Types

- **Large integers**: Max int64 values (`9223372036854775807`)
- **Negative numbers**: Including negative floats
- **Unicode strings**: Emojis, CJK characters, RTL text
- **Binary data**: All byte values 0-255
- **Empty collections**: Empty arrays, maps, strings
- **Null/Optional**: Missing optional fields

### Serialization

- **Roundtrip integrity**: `data == deserialize(serialize(data))`
- **Cross-format**: JSON → MsgPack → JSON consistency
- **Field ordering**: JSON key order independence
- **Type coercion**: Integer-float interoperability

### Error Handling

- **Malformed JSON**: Invalid syntax, truncated data
- **Corrupt MsgPack**: Invalid format bytes
- **Missing required fields**: Partial deserialization
- **Wrong types**: String where number expected

## Codecov Configuration

Coverage reports are uploaded to Codecov with these configurations:

```yaml
# codecov.yml
flags:
  typescript:
    paths: [generated/typescript/]
  python:
    paths: [generated/python/]
  # ... etc for all languages

component_management:
  individual_components:
    - component_id: typescript
      name: TypeScript
      paths: [generated/typescript/**]
```

### Path Fixes

Since tests run from `tests/` directories but coverage needs to map to `generated/`, path fixes are applied:

- `../../generated/typescript/` → `generated/typescript/`
- `crosspacket/packets/` → `generated/go/` (Go module path)
- `com/crosspacket/` → `generated/java/` (Java package path)

## Running Tests Locally

### All Languages (requires Docker)

```bash
# Use act to run GitHub Actions locally
act push -j test-java -P ubuntu-latest=catthehacker/ubuntu:act-latest
```

### Individual Languages

```bash
# TypeScript
cd tests/typescript && npm test

# Python
python -m pytest tests/python/ -v

# Go
cd generated/go && go test -v ./...

# Java
cd tests/java && mvn test

# C#
cd tests/csharp && dotnet test

# Dart
cd tests/dart && dart test

# PHP
cd tests/php && ./vendor/bin/phpunit

# Rust
cd tests/rust && cargo test

# C++
cd tests/cpp && ./test_catch2
```

## Continuous Integration

The CI workflow (`ci.yml`) runs on every push and PR:

1. **Matrix builds** - Tests across multiple language versions
2. **Parallel execution** - All languages test simultaneously
3. **Fail-fast disabled** - See all failures, not just first

The Coverage workflow runs after successful code generation:

1. **Triggered by**: Generate Code workflow completion
2. **Dependency**: Only runs on bot commits (not manual edits)
3. **Output**: Coverage badges via Codecov

## Contributing Tests

When adding new packet definitions:

1. **Add to definitions** (`definitions/packets/`)
2. **Regenerate code**: `python generate.py --all`
3. **Update tests** in each language's test directory
4. **Ensure coverage**: New code must have tests
5. **Run locally**: Verify all languages pass

### Test Naming Conventions

- Test class/file: `*Test*`, `*_test*`
- Test methods: `test_*`, `Test*`, `should*`
- Sections: Descriptive names like "MessagePacket JSON roundtrip"

## Troubleshooting

### Coverage Not Showing on Codecov

1. Check path fixes in `codecov.yml`
2. Verify generated/ folder is committed
3. Check upload logs in GitHub Actions
4. Ensure CODECOV_TOKEN secret is set

### Tests Failing with Import Errors

1. Ensure generated code is up-to-date: `python generate.py --all`
2. Check paths point to `generated/` not `output/`
3. Verify dependencies are installed

### C++ Compilation Errors

1. Check `std::optional` usage for optional fields
2. Verify include paths use `-I../../generated/cpp`
3. Ensure yyjson and msgpack-c are installed

## See Also

- [README.md](README.md) - Main project documentation
- [CONTRIBUTING.md](CONTRIBUTING.md) - How to contribute
- [codecov.yml](codecov.yml) - Codecov configuration
- [.github/workflows/coverage.yml](.github/workflows/coverage.yml) - Coverage workflow
