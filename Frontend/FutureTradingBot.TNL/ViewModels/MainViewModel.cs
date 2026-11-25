using CommunityToolkit.Mvvm.ComponentModel;

namespace BinanceFutureTradingBot.Desktop.ViewModels;

public partial class MainViewModel : ViewModelBase
{
    [ObservableProperty]
    public partial string AppTitle { get; set; } = "Binance Future Trading Bot";
}
