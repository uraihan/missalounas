class Restaurant:
    def __init__(self):
        pass

    def parse_response(self, id, raw_response):
        raise NotImplementedError()

    def get_restaurant_data(self, raw_response):
        raise NotImplementedError()
