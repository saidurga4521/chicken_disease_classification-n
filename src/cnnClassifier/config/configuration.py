from src.cnnClassifier.constants import *
import os
from src.cnnClassifier.utils.common import read_yaml,create_directories
from src.cnnClassifier.entity.config_entity import (DataIngestionConfig,
                                                    PrepareBaseModelConfig,
                                                    PrepareCallbacksConfig,
                                                    TrainingConfig)

class ConfigurationManager:
    def __init__(self,
                 config_file_path=CONFIG_FILE_PATH,
                 params_file_path=PARAMS_FILE_PATH):
        self.config=read_yaml(config_file_path)
        self.params=read_yaml(params_file_path)

        create_directories([self.config.artifacts_root])


    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config=self.config.data_ingestion 

        create_directories([config.root_dir])
        data_ingestion_config=DataIngestionConfig(
            root_dir=config.root_dir,
            source_URL=config.source_URL, 
            local_data_file=config.local_data_file,
            unzip_dir=config.unzip_dir
        )
        return data_ingestion_config
    
    def get_prepare_base_model_config(self) -> PrepareBaseModelConfig:
        config = self.config.prepare_base_model
        
        create_directories([config.root_dir])

        prepare_base_model_config = PrepareBaseModelConfig(
            root_dir=Path(config.root_dir),
            base_model_path=Path(config.base_model_path),
            updated_base_model_path=Path(config.updated_base_model_path),
            params_image_size=self.params.IMAGE_SIZE,
            params_learning_rate=self.params.LEARNING_RATE,
            params_include_top=self.params.INCLUDE_TOP,
            params_weights=self.params.WEIGHTS,
            params_classes=self.params.CLASSES
        )

        return prepare_base_model_config
    


    def get_prepare_callback_config(self) -> PrepareCallbacksConfig:
        try:
            config = self.config.prepare_callbacks
        except KeyError:
            # Handle the absence of 'prepare_callbacks' key, set default values, or raise an error.
            # For now, I'll set a default empty dictionary.
            config = {}

        model_ckpt_dir = os.path.dirname(config.get('checkpoint_model_filepath', ''))
        create_directories([
            Path(model_ckpt_dir),
            Path(config.get('tensorboard_root_log_dir', ''))
        ])

        prepare_callback_config = PrepareCallbacksConfig(
            root_dir=Path(config.get('root_dir', '')),
            tensorboard_root_log_dir=Path(config.get('tensorboard_root_log_dir', '')),
            checkpoint_model_filepath=Path(config.get('checkpoint_model_filepath', ''))
        )

        return prepare_callback_config
    
    

    def get_training_config(self) -> TrainingConfig:
        try:
            training = self.config.training
        except KeyError:
        # Handle the absence of 'training' key, set default values, or raise an error.
        # For now, I'll set a default empty dictionary.
            training = {}

        prepare_base_model = self.config.prepare_base_model
        params = self.params
        training_data = os.path.join(self.config.data_ingestion.unzip_dir, "Chicken-fecal-images")
        create_directories([
            Path(training.get('root_dir', ''))  # Use get() to handle missing key
    ])

        training_config = TrainingConfig(
           root_dir=Path(training.get('root_dir', '')),
           trained_model_path=Path(training.get('trained_model_path', '')),
           updated_base_model_path=Path(prepare_base_model.get('updated_base_model_path', '')),
           training_data=Path(training_data),
           params_epochs=params.get('EPOCHS', 0),  # Replace 0 with a suitable default value
           params_batch_size=params.get('BATCH_SIZE', 0),  # Replace 0 with a suitable default value
           params_is_augmentation=params.get('AUGMENTATION', False),  # Replace False with a suitable default value
           params_image_size=params.get('IMAGE_SIZE', 0)  # Replace 0 with a suitable default value
    )

        return training_config

        