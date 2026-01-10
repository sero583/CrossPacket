# Contributing to CrossPacket

Thank you for considering contributing to CrossPacket.

## How to Contribute

### Reporting Bugs

- Use the GitHub Issues tab
- Include your Python version, OS, and a minimal reproduction case
- Show the packets.json that causes the issue

### Feature Requests

- Open an issue with the `enhancement` label
- Describe the use case and expected behavior

### Pull Requests

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests: `python -m pytest tests/ -v`
5. Submit a PR with a clear description

## Code Style

Follow the official style guide for each language:

| Language   | Style Guide                   | Indentation |
| ---------- | ----------------------------- | ----------- |
| Python     | PEP 8                         | 4 spaces    |
| Dart       | dart.dev/effective-dart/style | 2 spaces    |
| Java       | Google Java Style             | 4 spaces    |
| TypeScript | Google TypeScript Style       | 2 spaces    |
| Rust       | rustfmt defaults              | 4 spaces    |
| Go         | gofmt                         | Tabs        |
| C++        | Google C++ Style              | 4 spaces    |
| C#         | Microsoft C# Style            | 4 spaces    |
| PHP        | PSR-12                        | 4 spaces    |

## Adding a New Language Generator

To add support for a new language:

1. Create a new generator class in `generate.py`:

   ```python
   class NewLanguageGenerator:
       def __init__(self, config: Dict[str, Any]):
           self.output_dir = Path(config.get("output_dir", "./output/newlang"))
           self.indent = "    "  # Follow language conventions

       def generate(self, packets: List[PacketDefinition], override: bool, clean: bool,
                    no_msgpack: bool = False, no_json: bool = False, type_field: str = "packetType"):
           self.type_field = type_field  # Store for use in serialization
           self.no_msgpack = no_msgpack
           self.no_json = no_json
           # Implementation here
           pass
   ```

2. Add type mappings in `TYPE_MAPPINGS` for the new language

3. Add CLI flag in `main()` function

4. Add tests in `tests/test_generator.py` (at minimum):

   - Generation test: Verify code generates without errors
   - Indentation test: Verify correct indentation style
   - Namespace/package test: Verify correct package declaration

5. Add runtime tests in `tests/newlang/` directory:

   - Serialization roundtrip (JSON and MessagePack)
   - All field types
   - Edge cases (empty strings, large numbers, unicode)

6. Update README.md with:

   - Language in supported languages table
   - Code examples in Quick Start section
   - Dependency information

7. Ensure the generator uses `self.type_field` for the packet type discriminator field

## Running Tests

CrossPacket has comprehensive test suites for all 9 languages. Each language uses its native testing framework.

### Generator Tests (Python)

```bash
# Install test dependencies
pip install pytest pytest-cov msgpack pyyaml

# Run all generator tests
python -m pytest tests/test_generator.py -v

# Run with coverage
python -m pytest tests/ --cov=generate --cov-report=html
```

### Language-Specific Tests

#### TypeScript (c8 + ts-node)

```bash
cd tests/typescript
npm install
npx c8 --reporter=lcov ts-node test_full_coverage.ts
```

#### Python (pytest)

```bash
pip install pytest pytest-cov msgpack
python -m pytest tests/python/ -v --cov=output/python
```

#### Java (Maven + JaCoCo)

```bash
cd tests/java
mvn test jacoco:report
# Coverage report: target/site/jacoco/index.html
```

#### Go (go test)

```bash
cd tests/go
go test -coverprofile=coverage.out -covermode=atomic ./...
go tool cover -html=coverage.out
```

#### C# (xUnit + Coverlet)

```bash
cd tests/csharp
dotnet test --collect:"XPlat Code Coverage"
```

#### Dart (flutter_test)

```bash
cd tests/dart
flutter pub get
flutter test --coverage
# Coverage: coverage/lcov.info
```

#### PHP (PHPUnit + Xdebug)

```bash
cd tests/php
composer install
php vendor/bin/phpunit --coverage-html coverage
```

#### Rust (cargo test)

```bash
cd tests/rust
cargo test
# For coverage: cargo tarpaulin or grcov
```

#### C++ (native tests)

```bash
cd tests/cpp
g++ -std=c++17 -I../../output/cpp test_comprehensive.cpp ../../output/cpp/*.cpp -lyyjson -o test_comprehensive
./test_comprehensive
```

### Coverage Requirements

We aim for high coverage across all languages:

| Language   | Target | Framework               |
| ---------- | ------ | ----------------------- |
| TypeScript | 95%+   | c8 + Jest/ts-node       |
| Python     | 95%+   | pytest-cov              |
| Java       | 95%+   | JaCoCo                  |
| Go         | 95%+   | go test -cover          |
| C#         | 95%+   | Coverlet                |
| Dart       | 95%+   | flutter test --coverage |
| PHP        | 90%+   | PHPUnit + Xdebug        |
| Rust       | N/A    | cargo test (passing)    |
| C++        | N/A    | Native tests (passing)  |

Coverage is automatically collected by CI and uploaded to [Codecov](https://codecov.io/gh/sero583/crosspacket).

## Test Structure

Each language should have:

1. **Generation tests** - Verify code generates without errors
2. **Syntax tests** - Verify generated code has valid syntax
3. **Serialization tests** - Verify JSON/MessagePack round-trips correctly
4. **Type field tests** - Verify configurable `type_field` is used correctly
5. **Constructor pattern tests** - Verify both empty constructor + setters and parameterized constructor work

Example test structure:

```python
def test_generates_valid_code():
    """Test that the generator produces valid code."""
    pass

def test_serialization_roundtrip():
    """Test that data survives serialize/deserialize cycle."""
    pass

def test_type_field_in_output():
    """Test that configurable type_field is used in generated code."""
    pass
```

## Reserved Field Names

The `type_field` configuration (default: `"packetType"`) is reserved and cannot be used as a field name. The generator validates this and will exit with an error if a conflict is detected.

## CI/CD Pipelines

CrossPacket uses GitHub Actions for continuous integration:

### Main CI (`ci.yml`)

Runs on every push and PR to `main`/`master`:

1. **Regenerates** all code from packets.json
2. **Tests** all 9 languages in parallel
3. **Uploads coverage** to Codecov

### Coverage Workflow (`coverage.yml`)

Collects coverage from all languages and uploads with language-specific flags to Codecov. Each language has its own flag for granular tracking.

### Local Development

Before submitting a PR, run the generator and tests locally:

```bash
# Regenerate all code
python generate.py --all --clean --override

# Run Python tests for the generator itself
python -m pytest tests/test_generator.py -v

# Run language-specific tests (pick your language)
cd tests/<language>
# Follow language-specific instructions above
```

## PHP msgpack on Windows

The PHP msgpack extension is not available as a pre-built binary for PHP 8.3+ on Windows. The official PECL Windows repository hasn't updated msgpack since 2022.

**Options for local development:**

1. **Docker** (recommended): Use the CI Docker environment which has msgpack installed:

   ```bash
   docker run --rm -v $(pwd):/app php:8.3-cli sh -c "pecl install msgpack && echo 'extension=msgpack.so' >> /usr/local/etc/php/php.ini && php vendor/bin/phpunit"
   ```

2. **WSL (Windows Subsystem for Linux)**: Install PHP with pecl in WSL:

   ```bash
   sudo apt install php8.3 php8.3-dev php-pear
   sudo pecl install msgpack
   ```

3. **Generate without MessagePack**: For local testing, use `--no-msgpack`:

   ```bash
   python generate.py --all --no-msgpack
   ```

   This generates code with JSON-only serialization.

4. **PHP 8.0/8.1**: If you must use native Windows PHP with msgpack, use PHP 8.0 or 8.1 which has pre-built DLLs available.

**CI Environment**: Our GitHub Actions CI runs PHP tests in a Linux environment where msgpack is installed via pecl. Coverage is collected and uploaded to Codecov.

## Questions?

Open an issue with the `question` label.
