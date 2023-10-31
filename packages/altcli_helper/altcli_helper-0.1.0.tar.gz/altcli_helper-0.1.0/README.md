# CLIHelper: A Command-Line Interface Assistant

CLIHelper is a command-line interface (CLI) tool designed to assist users by generating CLI commands or a series of CLI commands based on user input. Utilizing OpenAI's GPT model, it provides detailed responses and ensures a comprehensive understanding of the required tasks.

## Installation

This tool can be installed using Poetry. Ensure you have Poetry installed on your machine. If not, you can install it following the instructions on the [official Poetry website](https://python-poetry.org/docs/).

Once Poetry is installed, you can install CLIHelper with the following command:

```sh
poetry install
```

## Usage

CLIHelper is straightforward to use and can be executed directly from the command line.

### Basic Command Generation

For generating a CLI command based on your request:

```sh
clih "Your request here"
```

Example:

```sh
clih "How to list all files in a directory?"
```

### Command Generation with Rationale

If you want to see the rationale behind the recommended commands, in addition to the commands themselves, use the `-s` or `--show-rationale` flag:

```sh
clih -s "Your request here"
```

or

```sh
clih --show-rationale "Your request here"
```

Example:

```sh
clih -s "How to list all files in a directory?"
```

This will print out a detailed rationale explaining why certain commands are recommended, followed by the recommended commands themselves.

## Contact

For any inquiries or issues, please contact D0rkKnight at [shouhanzen@gmail.com](mailto:shouhanzen@gmail.com).

## License

This project is open source and available under the [MIT License](LICENSE).

---

The README provides a concise yet comprehensive guide on how to install and use CLIHelper, including both basic command generation and command generation with rationale functionalities. It also includes contact information for support. Make sure to include an actual LICENSE file in your project if you mention it in the README.
