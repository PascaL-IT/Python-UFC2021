# Http Client to retrieve piza list from Heroku via REST API (URL)
import json

from kivy.clock import Clock
from kivy.network.urlrequest import UrlRequest
from models import Pizza


class HttpClient():

    # See constants & collections : https://docs.python.org/2/library/collections.html#collections.namedtuple
    API_URL1 = "https://pizzamama-pl1.herokuapp.com/api/GetPizzas"
    API_URL2 = "https://jrpizzamamadjango2.herokuapp.com/api/GetPizzas"

    # Retrieve the pizzas asynchronously
    def get_pizzas(self, fct_on_sucess, fct_on_error, fct_on_failure, fct_on_progress):

        # Internal function - called asynchronously by UrlRequest
        def got_pizza_json(request, result):
            pizzas_data = json.loads(result)   # deserialise in Python array/list of k:v
            print("got_pizza_json -> on_success")
            if fct_on_sucess:
                fct_on_sucess(pizzas_data) # callback to return pizzas data

        def do_on_redirect(request, result):
            print("do_on_redirect -> ?")

        def do_on_failure(request, result):
            print("on_failure -> resp_status")
            if fct_on_failure:
                fct_on_failure("FAILURE - " + str(request.resp_status)) # callback to return a failure message

        def do_on_error(request, error):
            print("do_on_error -> error")
            if fct_on_error:
                fct_on_error("ERROR - " + str(error))  # callback to return an error message

        def do_on_progress(request, current_size, total_size):
            ratio = current_size/total_size
            print("do_on_progress -> ratio")
            if fct_on_progress:
                fct_on_progress(ratio)

        def do_on_cancel(request):
            print("do_on_cancel -> ?")

        # Request on URL - GET on REST API
        request = UrlRequest(self.API_URL1,
                             on_success=got_pizza_json,
                                on_redirect=do_on_redirect,
                                    on_failure=do_on_failure,
                                        on_error=do_on_error,
                                            on_progress=do_on_progress,
                                                on_cancel=do_on_cancel,
                                                    method="GET",
                                                        chunk_size=10)



        # request.wait(2.0)  # synchrone
        # print("list of pizza objects: " + str(self.pizzas))
        # return self.pizzas
