from argparse import ArgumentParser

import pytorch_lightning as pl
from torch.utils.data import DataLoader, random_split
from torchvision import transforms
from torchvision.datasets import ImageFolder, CIFAR10

from backbones import DummyBackbone, ResnetBackbone
from classifier import Classifier


def parse_args(args=None):
    parser = ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='./data')
    parser.add_argument('--batch_size', type=int, default=32)
    parser.add_argument('--lr', type=float, default=1e-3)
    parser.add_argument('--freeze_resnet', action='store_true')
    parser.add_argument('--num_workers', type=int, default=8)
    parser.add_argument('--split_size', type=int, default=2500)
    parser.add_argument('--seed', type=int, default=42)
    parser = pl.Trainer.add_argparse_args(parser)
    return parser.parse_args(args)


if __name__ == '__main__':
    args = parse_args()

    # Transforms
    transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(256),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

    # Backbone
    backbone = ResnetBackbone(256, 2, freeze_resnet=args.freeze_resnet)

    # Data
    data = ImageFolder(root=args.data_dir, transform=transform)
    train_ds, val_ds = random_split(data, [len(data) - args.split_size, args.split_size])
    train_loader = DataLoader(train_ds, batch_size=args.batch_size, num_workers=args.num_workers)
    val_loader = DataLoader(val_ds, batch_size=args.batch_size, num_workers=args.num_workers)

    # Model
    model = Classifier(backbone, learning_rate=args.lr)
    
    # Train
    trainer = pl.Trainer.from_argparse_args(args)
    trainer.fit(model, train_loader, val_loader)
