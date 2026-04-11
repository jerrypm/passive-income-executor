import Combine

enum HomeState {
    case loading, loaded([HomeItem]), empty, error(String)
}

class HomePresenter: ObservableObject {
    @Published var state: HomeState = .loading

    private let interactor: HomeInteractorProtocol

    init(interactor: HomeInteractorProtocol) {
        self.interactor = interactor
    }

    @MainActor
    func fetchItems() async {
        state = .loading
        do {
            let items = try await interactor.fetchItems()
            state = items.isEmpty ? .empty : .loaded(items)
        } catch {
            state = .error(error.localizedDescription)
        }
    }
}
