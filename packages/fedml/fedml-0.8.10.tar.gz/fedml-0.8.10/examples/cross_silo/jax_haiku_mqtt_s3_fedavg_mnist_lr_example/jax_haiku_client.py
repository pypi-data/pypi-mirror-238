import fedml

from fedml import FedMLRunner
from fedml.data.MNIST.data_loader import download_mnist, load_partition_data_mnist
from jax_haiku_model import create_model
from jax_haiku_model_trainer_classification import JaxHaikuModelTrainerCLS


def load_data(args):
    download_mnist(args.data_cache_dir)
    fedml.logging.info("load_data. dataset_name = %s" % args.dataset)

    """
    Please read through the data loader at to see how to customize the dataset for FedML framework.
    """
    (
        client_num,
        train_data_num,
        test_data_num,
        train_data_global,
        test_data_global,
        train_data_local_num_dict,
        train_data_local_dict,
        test_data_local_dict,
        class_num,
    ) = load_partition_data_mnist(
        args,
        args.batch_size,
        train_path=args.data_cache_dir + "/MNIST/train",
        test_path=args.data_cache_dir + "/MNIST/test",
    )
    """
    For shallow NN or linear models, 
    we uniformly sample a fraction of clients each round (as the original FedAvg paper)
    """
    args.client_num_in_total = client_num
    dataset = [
        train_data_num,
        test_data_num,
        train_data_global,
        test_data_global,
        train_data_local_num_dict,
        train_data_local_dict,
        test_data_local_dict,
        class_num,
    ]
    return dataset, class_num


def create_model_trainer(in_model, in_args):
    model_trainer = JaxHaikuModelTrainerCLS(in_model, in_args)
    return model_trainer


if __name__ == "__main__":
    # init FedML framework
    args = fedml.init()

    # init device
    device = fedml.device.get_device(args)

    # load data
    dataset, output_dim = load_data(args)

    # load model (the size of MNIST image is 28 x 28)
    model = create_model(28 * 28, output_dim)

    # create model trainer
    trainer = create_model_trainer(model, args)

    # start training
    fedml_runner = FedMLRunner(args, device, dataset, model, client_trainer=trainer)
    fedml_runner.run()
