import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Tuple, Optional


class EMGMultiInputModel(nn.Module):
    """
    Hybrid neural network for EMG gesture recognition.
    
    This model combines:
    1. CNN branch for processing raw EMG signals
    2. MLP branch for processing hand-crafted features
    3. Combined classifier for final gesture prediction
    
    Architecture:
    - Signal Branch: 3 conv layers + global pooling
    - Feature Branch: 2 fully connected layers
    - Classifier: 3 fully connected layers with dropout
    """
    
    def __init__(self, signal_length: int = 250, num_features: int = 4, 
                 num_classes: int = 4, hidden_size: int = 128):
        """
        Initialize the multi-input EMG model.
        
        Args:
            signal_length: Length of EMG signal window
            num_features: Number of hand-crafted features
            num_classes: Number of gesture classes
            hidden_size: Size of hidden layers
        """
        super(EMGMultiInputModel, self).__init__()
        
        # Signal processing branch (CNN for temporal features)
        self.signal_encoder = nn.Sequential(
            # First conv layer: 1 -> 32 channels, kernel=7, stride=2
            nn.Conv1d(1, 32, kernel_size=7, stride=2, padding=3),
            nn.BatchNorm1d(32),
            nn.ReLU(),
            nn.Dropout(0.2),
            
            # Second conv layer: 32 -> 64 channels, kernel=5, stride=2
            nn.Conv1d(32, 64, kernel_size=5, stride=2, padding=2),
            nn.BatchNorm1d(64),
            nn.ReLU(),
            nn.Dropout(0.2),
            
            # Third conv layer: 64 -> 128 channels, kernel=3, stride=1
            nn.Conv1d(64, 128, kernel_size=3, stride=1, padding=1),
            nn.BatchNorm1d(128),
            nn.ReLU(),
            nn.Dropout(0.2),
            
            # Global average pooling to get fixed-size representation
            nn.AdaptiveAvgPool1d(1)
        )
        
        # Feature processing branch (MLP for hand-crafted features)
        self.feature_encoder = nn.Sequential(
            nn.Linear(num_features, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Dropout(0.3)
        )
        
        # Combined classifier
        signal_features = 128  # Output size from CNN branch
        feature_features = hidden_size // 2  # Output size from MLP branch
        combined_size = signal_features + feature_features
        
        self.classifier = nn.Sequential(
            nn.Linear(combined_size, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Dropout(0.4),
            nn.Linear(hidden_size // 2, num_classes)
        )
        
    def forward(self, signal: torch.Tensor, features: torch.Tensor) -> torch.Tensor:
        """
        Forward pass with two inputs.
        
        Args:
            signal: EMG signal tensor of shape (batch_size, signal_length)
            features: Feature tensor of shape (batch_size, num_features)
            
        Returns:
            Logits of shape (batch_size, num_classes)
        """
        # Process signal through CNN
        # Add channel dimension: (batch_size, signal_length) -> (batch_size, 1, signal_length)
        signal = signal.unsqueeze(1)
        signal_features = self.signal_encoder(signal)
        signal_features = signal_features.squeeze(-1)  # Remove last dimension
        
        # Process features through MLP
        feature_encoding = self.feature_encoder(features)
        
        # Combine both representations
        combined = torch.cat([signal_features, feature_encoding], dim=1)
        
        # Classify
        output = self.classifier(combined)
        
        return output


class EMGSimpleModel(nn.Module):
    """
    Simple baseline model that only uses hand-crafted features.
    
    This model serves as a baseline for comparison with the hybrid model.
    It processes only the extracted features without using raw signal data.
    """
    
    def __init__(self, num_features: int = 4, num_classes: int = 4, 
                 hidden_size: int = 64):
        """
        Initialize the simple feature-based model.
        
        Args:
            num_features: Number of input features
            num_classes: Number of gesture classes
            hidden_size: Size of hidden layers
        """
        super(EMGSimpleModel, self).__init__()
        
        self.classifier = nn.Sequential(
            nn.Linear(num_features, hidden_size),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_size, hidden_size // 2),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(hidden_size // 2, num_classes)
        )
    
    def forward(self, features: torch.Tensor) -> torch.Tensor:
        """
        Forward pass using only features.
        
        Args:
            features: Feature tensor of shape (batch_size, num_features)
            
        Returns:
            Logits of shape (batch_size, num_classes)
        """
        return self.classifier(features)


def create_model(model_type: str = 'multi_input', **kwargs) -> nn.Module:
    """
    Factory function to create EMG models.
    
    Args:
        model_type: 'multi_input' or 'simple'
        **kwargs: Model parameters
        
    Returns:
        Initialized model instance
        
    Raises:
        ValueError: If model_type is not recognized
    """
    if model_type == 'multi_input':
        return EMGMultiInputModel(**kwargs)
    elif model_type == 'simple':
        return EMGSimpleModel(**kwargs)
    else:
        raise ValueError(f"Unknown model type: {model_type}")


def test_model() -> EMGMultiInputModel:
    """
    Test the model with sample data to verify architecture.
    
    Returns:
        The tested model instance
    """
    print("🧪 Testing EMG Multi-Input Model...")
    
    # Create model
    model = EMGMultiInputModel(signal_length=250, num_features=4, num_classes=4)
    model.eval()
    
    # Create sample data
    batch_size = 2
    signal = torch.randn(batch_size, 250)  # (batch_size, signal_length)
    features = torch.randn(batch_size, 4)  # (batch_size, num_features)
    
    # Forward pass
    with torch.no_grad():
        output = model(signal, features)
        
        print(f"✅ Model test successful!")
        print(f"📊 Input signal shape: {signal.shape}")
        print(f"📊 Input features shape: {features.shape}")
        print(f"📊 Output shape: {output.shape}")
        print(f"🎯 Predictions: {torch.argmax(output, dim=1)}")
        
        # Calculate model parameters
        total_params = sum(p.numel() for p in model.parameters())
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        print(f"📈 Total parameters: {total_params:,}")
        print(f"📈 Trainable parameters: {trainable_params:,}")
    
    return model


def get_model_summary(model: nn.Module) -> str:
    """
    Generate a summary of model architecture and parameters.
    
    Args:
        model: PyTorch model to summarize
        
    Returns:
        Formatted string with model summary
    """
    total_params = sum(p.numel() for p in model.parameters())
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    
    summary = f"""
Model Summary:
==============
Model Type: {model.__class__.__name__}
Total Parameters: {total_params:,}
Trainable Parameters: {trainable_params:,}
Model Size: {total_params * 4 / 1024:.1f} KB (float32)

Architecture:
"""
    
    for name, module in model.named_children():
        if isinstance(module, nn.Sequential):
            summary += f"\n{name}:\n"
            for i, layer in enumerate(module):
                summary += f"  {i+1}. {layer}\n"
        else:
            summary += f"\n{name}: {module}\n"
    
    return summary


if __name__ == "__main__":
    # Test the model
    model = test_model()
    
    # Print model summary
    print(get_model_summary(model))
