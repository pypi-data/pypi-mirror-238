from . import Logger
from Omnicon_GenericDDSEngine_Py import Omnicon_GenericDDSEngine_Py as Omnicon


class OmniconEngineHandler:
    def __init__(self, input_files_and_dirs_list: list, is_parse_ROS2_constants: bool):

        self.logger = Logger.add_logger(__name__)
        self.engine = None
        self.init_and_run_engine(input_files_and_dirs_list, is_parse_ROS2_constants)

    @staticmethod
    def set_engines_factory_verbosity( logging_verbosity: str):
        verbosity = OmniconEngineHandler.get_engine_log_level(logging_verbosity)

        factory_configuration = Omnicon.FactoryConfiguration()
        factory_configuration.loggerConfiguration.verbosity = verbosity
        Omnicon.GenericDDSEngine.SetFactoryConfiguration(factory_configuration)

    @staticmethod
    def get_engine_log_level( logging_verbosity: str):
        logging_verbosity = logging_verbosity.lower()
        verbosity_dict = {
            "fatal": Omnicon.LogSeverityLevel.fatal,
            "error": Omnicon.LogSeverityLevel.error,
            "warning": Omnicon.LogSeverityLevel.warning,
            "info": Omnicon.LogSeverityLevel.info,
            "debug": Omnicon.LogSeverityLevel.debug,
            "trace": Omnicon.LogSeverityLevel.trace
            }
        if logging_verbosity not in verbosity_dict.keys():
            raise Exception(f"Logging verbosity '{logging_verbosity}' is invalid. "
                            f"Please use 'FATAL'/ 'ERROR'/ 'WARNING'/ 'INFO' or 'DEBUG'")
        return verbosity_dict[logging_verbosity]

    def init_and_run_engine(self, input_files_and_dirs_list: list,
                            is_parse_ROS2_constants: bool) -> Omnicon.GenericDDSEngine:
        """
        This creates an engine instance and performs init and run with the desired configurations.
        :param input_files_and_dirs_list: A string that holds the path of the folder that holds the input_pointer files
        """
        # Create an engine instance:
        self.engine = Omnicon.GenericDDSEngine()


        # Create an engine configuration object:
        engine_configuration = Omnicon.EngineConfiguration()
        # Set the parameters:
        engine_configuration.threadPoolSize = 3
        # Go over the new list and append it into the configuration file path vector:
        for input_file in input_files_and_dirs_list:
            engine_configuration.ddsConfigurationFilesPath.append(input_file)
        # Perform the introspection:
        engine_configuration.engineOperationMode = \
            Omnicon.EngineOperationMode.TYPE_INTROSPECTION
        engine_configuration.parseROS2Constants = is_parse_ROS2_constants
        # init the engine:
        self.logger.debug("init engine...")

        self.engine.Init(engine_configuration)
        self.logger.info("Engine was init successfully")
        # Run the engine:
        self.engine.Run()
        # When Init() went well, make a log entry:
        self.logger.debug("Engine is now up and running")

    def shutdown_engine(self):
        try:
            self.logger.debug("Shutting down Omnicon engine")
            if self.engine:
                self.engine.Shutdown()
                del self.engine
                self.engine = None
            self.logger.debug("Engine shutdown is complete")
        except Exception as error:
            self.logger.error("shutdown_introspection_engine exception occurred:", error)
