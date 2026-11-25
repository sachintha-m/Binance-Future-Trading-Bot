using Avalonia.Controls;
using Avalonia.Input;
using Avalonia.Interactivity;

namespace FutureTradingBot.TNL.Controls;

public partial class TitleBarControl : UserControl
{
    public TitleBarControl()
    {
        InitializeComponent();
    }
    
    private Window? HostWindow => TopLevel.GetTopLevel(this) as Window;

    private void TitleBar_PointerPressed(object? sender, PointerPressedEventArgs e)
    {
        if (HostWindow is not { } window)
            return;
        var point = e.GetCurrentPoint(this);
        if (!point.Properties.IsLeftButtonPressed)
            return;
        if (e.ClickCount == 2)
        {
            window.WindowState = window.WindowState == WindowState.Maximized
                ? WindowState.Normal
                : WindowState.Maximized;
            return;
        }
        window.BeginMoveDrag(e);
    }

    private void Minimize_Click(object? sender, RoutedEventArgs e)
    {
        if (HostWindow is not { } window)
            return;
        window.WindowState = WindowState.Minimized;
    }

    private void Maximize_Click(object? sender, RoutedEventArgs e)
    {
        if (HostWindow is not { } window)
            return;
        window.WindowState = window.WindowState == WindowState.Maximized
            ? WindowState.Normal
            : WindowState.Maximized;
    }
    
    private void Close_Click(object? sender, RoutedEventArgs e)
    {
        HostWindow?.Close();
    }
}