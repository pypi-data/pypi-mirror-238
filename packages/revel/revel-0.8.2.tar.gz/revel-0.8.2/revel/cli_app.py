import sys
from dataclasses import KW_ONLY, dataclass
from typing import *  # type: ignore

from . import argument_parser, common
from .errors import (
    AmbiguousOptionError,
    ArgumentError,
    NoOptionGivenError,
    NoSuchOptionError,
)
from .legacy import error, print, warning


@dataclass(frozen=True)
class Parameter:
    name: str
    _ = KW_ONLY
    summary: Optional[str] = None


@dataclass(frozen=True)
class AppCommand:
    # The name to use for this command
    name: str

    # Short description of the command
    summary: Optional[str]

    # Longer, detailed description of the command
    details: Optional[str]

    # Any parameters the user has provided to describe this command. These may
    # be fewer than the function's parameters, or empty altogether.
    user_provided_parameters: List[Parameter]

    # The function to call when this command is invoked
    function: Callable


class App:
    def __init__(
        self,
        *,
        summary: Optional[str] = None,
        details: Optional[str] = None,
        add_help_command: bool = True,
        add_version_command: bool = True,
    ):
        self.summary = summary
        self.details = details
        self._commands: List[AppCommand] = []

        # Add built-in commands
        if add_help_command:
            self.command(
                name="help",
                summary="Display help for a command",
                details="""
If not command is provided, this command will show general help for the
application. If a command is provided, shows help for that command instead.
                """,
            )(self._display_help)

        if add_version_command:
            self.command(
                name="version",
                summary="Display the application's version",
            )(self._display_version)

    def _display_help(self, command: Optional[str] = None) -> None:
        # Was an invalid command specified?
        cmd_instance: Optional[AppCommand] = None

        if command is not None:
            try:
                cmd_index = common.choose_string(
                    [[cmd.name] for cmd in self._commands], command
                )
            except NoSuchOptionError as err:
                error(f"There is no command named `{err.entered_command}`")
                print()
            except AmbiguousOptionError as err:
                error(err.message)
                print()
            else:
                cmd_instance = self._commands[cmd_index]

        # If not command was provided, or the given one doesn't exist, display
        # general help
        if cmd_instance is None:
            # Summary
            if self.summary is not None:
                print(self.summary)
                print()

            # Usage
            print(f"[dim]Usage:[/] {sys.argv[0]} <command> [[options]")
            print()

            # Details
            if self.details is not None:
                print(self.details)
                print()

            # Commands
            print(f"Available commands are:")
            align_len = max(len(cmd.name) for cmd in self._commands)
            self._commands.sort(key=lambda cmd: cmd.name.lower())

            for cmd_instance in self._commands:
                if cmd_instance.summary is None:
                    summary = ""
                else:
                    summary = f"  ...  {cmd_instance.summary}"

                print(f"  [blue]{cmd_instance.name:<{align_len}}[/]{summary}")

            return

        # A command was provided. Display information about that command
        # specifically
        assert cmd_instance is not None, cmd_instance
        if cmd_instance.summary is None:
            print(f"[bold blue]{cmd_instance.name}[/]")
        else:
            print(f"[bold blue]{cmd_instance.name}[/]  \u2014  {cmd_instance.summary}")

        # Usage
        print()
        parsed_parameters = list(
            argument_parser.parameters_from_function(cmd_instance.function)
        )

        params_str = ""
        for inspect_param, revel_param in parsed_parameters:
            # Format the parameter
            is_optional = revel_param.default_value is not argument_parser.NO_DEFAULT

            if not is_optional and not revel_param.is_flag:
                param_str = f"<{revel_param.name}>"
            else:
                if revel_param.is_flag:
                    param_str = f"--{revel_param.name} <value>"
                else:
                    param_str = revel_param.name

                if is_optional:
                    param_str = f"[[{param_str}]"

            params_str += f" {param_str}"

        print(f"[dim]Usage:[/] {sys.argv[0]} {cmd_instance.name}{params_str}")

        # Parameter descriptions
        if parsed_parameters:
            print()
            name_to_user_param = {
                param.name: param for param in cmd_instance.user_provided_parameters
            }

            align_len = max(len(params[1].name) for params in parsed_parameters)

            for inspect_param, revel_param in parsed_parameters:
                line = f"  [blue]{revel_param.name:<{align_len}}[/]"

                # Summary
                try:
                    user_param = name_to_user_param[inspect_param.name]
                except KeyError:
                    pass
                else:
                    if user_param.summary is not None:
                        line += f"  ...  {user_param.summary}"

                # Default value
                if isinstance(
                    revel_param.default_value, (bool, int, float, str, type(None))
                ):
                    line += f"  [dim](defaults to {revel_param.default_value})[/]"
                elif revel_param.default_value is not argument_parser.NO_DEFAULT:
                    line += f"  [dim](optional)[/]"

                print(line)

        # Details
        if cmd_instance.details is not None:
            print()
            print(cmd_instance.details)

    def _display_version(self) -> None:
        # TODO: Find the version
        name = "<TODO: Name>"
        version = "<TODO: Version>"

        # Display it
        print(f"{name} {version}")

    def command(
        self,
        *,
        name: Optional[str] = None,
        summary: Optional[str] = None,
        details: Optional[str] = None,
        parameters: Iterable[Parameter] = [],
    ):
        """
        Register a function as a command, allowing users to call the function
        from the CLI. The function's name will be used as the command's name.
        """

        # Prepare the arguments
        if name is not None:
            name = name.strip()

        if summary is not None:
            summary = summary.strip()

        if details is not None:
            details = details.strip()

        parameters = list(parameters)

        # Create the decorator
        def result(func: Callable) -> Callable:
            # Parse all parameters this function has
            parsed_parameters = {
                params[0].name: params[0]
                for params in argument_parser.parameters_from_function(func)
            }

            # Make sure the user-provided parameters match the function's
            for uparam in parameters:
                if uparam.name not in parsed_parameters:
                    raise ValueError(
                        f"This function has no parameter named `{uparam.name}`"
                    )

            # Register the command
            self._commands.append(
                AppCommand(
                    name=common.python_name_to_console(func.__name__)
                    if name is None
                    else name,
                    summary=summary,
                    details=details,
                    function=func,
                    user_provided_parameters=parameters,
                )
            )

            return func

        return result

    def run(self, args: Optional[Iterable[str]] = None) -> None:
        if args is None:
            args = sys.argv
        else:
            args = list(args)

        # Delegate to the argument parser to call the correct command
        #
        # TODO: What if there is only one command? Should it still have to be
        # specified?

        # FIXME: This is imperfect, as it actually allows the user to specify
        # "exit" as a command, despite that obviously not being one.
        self._commands.sort(key=lambda cmd: cmd.name.lower())
        options = {cmd.name: cmd.function for cmd in self._commands}
        options["Exit"] = lambda: sys.exit(0)

        try:
            argument_parser.call_functions(
                options,
                sys.argv[1:],
                interactive=True,
            )

        # The user has cancelled the command
        except KeyboardInterrupt:
            print()
            print("[yellow]Canceled[/]")
            sys.exit(1)

        # No option provided
        except NoOptionGivenError as err:
            error(err.message)
            print()
            self._display_help()
            sys.exit(1)

        # Invalid command: Display the error, as well as help
        except NoSuchOptionError as err:
            error(err.message)
            print()
            self._display_help()
            sys.exit(1)

        # Ambiguous command: Display the error, as well as help
        except AmbiguousOptionError as err:
            error(err.message)
            print()
            self._display_help()
            sys.exit(1)

        # Invalid Arguments
        except ArgumentError as err:
            error(err.message)
            sys.exit(1)
