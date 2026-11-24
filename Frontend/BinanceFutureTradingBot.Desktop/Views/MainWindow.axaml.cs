using Avalonia;
using Avalonia.Controls;
using Avalonia.Interactivity;

namespace BinanceFutureTradingBot.Desktop.Views;

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
            RootBorder.CornerRadius = WindowState == WindowState.Maximized
                ? default
                : new CornerRadius(12);
        }
    }

    private void Minimize_Click(object? sender, RoutedEventArgs e)
    {
        WindowState =  WindowState.Minimized;
    }

    private void Maximize_Click(object? sender, RoutedEventArgs e)
    {
        WindowState =  WindowState == WindowState.Maximized
            ? WindowState.Normal
            : WindowState.Maximized;
    }
    
    private void Close_Click(object? sender, RoutedEventArgs e)
    {
        Close();
    }
}