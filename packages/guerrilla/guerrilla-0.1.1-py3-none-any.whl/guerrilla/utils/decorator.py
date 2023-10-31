from functools import wraps
from guerrilla.device.router.mode import MODE
from guerrilla.device.router import Commands


def root_access_required(func):
    @wraps(func)
    def wrapper(service_instance, *args, **kwargs):
        # Get the session from the service_instance
        session = service_instance._ssh
        # Login as root
        session.login_as_root()
        # Call the original function with the given arguments and keyword arguments
        result = func(service_instance, *args, **kwargs)
        # Logout from root
        session.logout_from_root()

        return result

    return wrapper


def mode(target_mode, additional_command=None):
    def transition_mode(self, from_mode, to_mode):
        match (to_mode, from_mode):
            case (MODE.MAIN, MODE.CONFIG):
                self.run(Commands.SYSTEM.EXIT)
            case (MODE.MAIN, MODE.CONFIG_IF):
                self.run(Commands.SYSTEM.EXIT)
                self.run(Commands.SYSTEM.EXIT)
            case (MODE.CONFIG, MODE.MAIN):
                self.run(Commands.SYSTEM.CONFIGURE)
            case (MODE.CONFIG, MODE.CONFIG_IF):
                self.run(Commands.SYSTEM.EXIT)
            case (MODE.CONFIG_IF, MODE.MAIN):
                self.run(Commands.SYSTEM.CONFIGURE)
                if additional_command:
                    self.run(additional_command)
            case (MODE.CONFIG_IF, MODE.CONFIG):
                if additional_command:
                    self.run(additional_command)
            case _:
                pass  # Do nothing

    def decorator(func):
        @wraps(func)
        def wrapper(self, *fargs, **fkwargs):
            current_mode = self.check_mode()

            # Transition to the target mode
            transition_mode(self, current_mode, target_mode)

            result = func(self, *fargs, **fkwargs)

            # Return to the original mode
            transition_mode(self, target_mode, current_mode)

            return result

        return wrapper

    # Check if target_mode is 'config-if' and no additional_command is provided
    if target_mode == MODE.CONFIG_IF and additional_command is None:
        raise ValueError(
            "For 'config-if' mode, an additional_command must be provided."
        )

    return decorator
