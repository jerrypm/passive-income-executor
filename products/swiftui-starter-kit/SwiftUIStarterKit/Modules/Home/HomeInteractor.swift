import Foundation

protocol HomeInteractorProtocol {
    func fetchItems() async throws -> [HomeItem]
}

class HomeInteractor: HomeInteractorProtocol {
    private let apiClient: APIClientProtocol

    init(apiClient: APIClientProtocol = MockAPIClient.shared) {
        self.apiClient = apiClient
    }

    func fetchItems() async throws -> [HomeItem] {
        try await apiClient.request(HomeEndpoint.fetchItems)
    }
}
