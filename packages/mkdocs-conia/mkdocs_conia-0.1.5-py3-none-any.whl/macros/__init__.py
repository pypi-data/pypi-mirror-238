def define_env(env):
    @env.macro
    def php(function):
        return f"[`{function}`](https://php.net/{function})"
