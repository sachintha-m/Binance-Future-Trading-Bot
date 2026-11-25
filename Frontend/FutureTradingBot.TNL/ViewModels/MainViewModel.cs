using CommunityToolkit.Mvvm.ComponentModel;

namespace FutureTradingBot.TNL.ViewModels;

public partial class MainViewModel : ViewModelBase
{
    [ObservableProperty]
    public partial string AppTitle { get; set; } = "Future Trading Bot - TNL";
}
