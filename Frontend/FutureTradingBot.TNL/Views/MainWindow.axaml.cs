using Avalonia;
using Avalonia.Controls;

namespace FutureTradingBot.TNL.Views;

public partial class MainWindow : Window
{
    public MainWindow()
    {
        InitializeComponent();
    }

    protected override void OnPropertyChanged(AvaloniaPropertyChangedEventArgs change)
    {
        base.OnPropertyChanged(change);
    
        if (change.Property == WindowStateProperty && RootBorder is not null)
        {
            var isMaximized = WindowState == WindowState.Maximized;
            
            RootBorder.CornerRadius = isMaximized
                ? default
                : new CornerRadius(12);
            RootBorder.Margin = isMaximized
                ? default
                : new Thickness(24);
        }
    }
}