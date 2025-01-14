import google.generativeai as genai
import openai
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import ChatHistory, RoomTable, RestaurantTable, RentedVehicle, Spot
from .serializers import RoomTableSerializer, RestaurantTableSerializer, RentedVehicleSerializer, SpotSerializer

# Initialize Google Gemini API
genai.configure(api_key="AIzaSyA0USMpFTzWEzYM3EqiTyXCYKKdbeZ9BIE")  # Replace with your Gemini API key

# Initialize OpenAI API
openai.api_key = 'YOUR_OPENAI_API_KEY'  # Replace with your OpenAI API key
class ItineraryView(APIView):
    def post(self, request):
        # Get query from the user input
        user_query = request.data.get('query', '')
        budget = request.data.get('budget', 1000)  # Extract budget from the request if provided, default to 1000 INR

        # Default response if no input
        response_data = {
            'rooms': [],
            'rented_vehicles': [],
            'nearby_spots': {
                'free_entry_spots': [],
                'paid_spots': []
            },
            'restaurants': [],
            'chatbot_response': "",
            "chat_history": [],   # This will store the chatbot-like response
        }

        # Fetch data from the models and filter based on budget if needed
        rooms_data = RoomTable.objects.filter(price__lte=budget)  # Filter rooms within the user's budget
        rented_vehicles_data = RentedVehicle.objects.filter(rent__lte=budget)  # Filter vehicles within the budget
        free_spots_data = Spot.objects.filter(ticket="free")  # Get free-entry spots
        paid_spots_data = Spot.objects.filter(ticket="paid")  # Get paid spots
        restaurants_data = RestaurantTable.objects.all()  # Get all restaurants (no budget filter for restaurants)

        # Serialize the data to pass it to the Gemini API in a structured way
        rooms_list = RoomTableSerializer(rooms_data, many=True).data
        vehicles_list = RentedVehicleSerializer(rented_vehicles_data, many=True).data
        free_spots_list = SpotSerializer(free_spots_data, many=True).data
        paid_spots_list = SpotSerializer(paid_spots_data, many=True).data
        restaurants_list = RestaurantTableSerializer(restaurants_data, many=True).data

        # Prepare the spots data, adding the ticket charge for paid spots
        paid_spots_info = []
        for spot in paid_spots_list:
            spot_info = {
                "placename": spot['placename'],
                "description": spot['description'],
                "ticket_charge": spot['ticket_charge']
            }
            paid_spots_info.append(spot_info)

        # Construct the prompt using the filtered data (ensure it's only from the models)
        print(user_query,vehicles_list,paid_spots_info,free_spots_list,restaurants_list)
        prompt = (
            f"User Query: {user_query}. "
            f"The available rooms are: {rooms_list}, "
            f"the available rented vehicles are: {vehicles_list}, "
            f"the free-entry spots are: {free_spots_list}, "
            f"the paid spots are: {paid_spots_info}, "
            f"and the restaurants are: {restaurants_list}. "
            f"Include only recommendations from rooms {rooms_list} ,from vehicles {vehicles_list},spots_list{free_spots_list},paid spot_list{paid_spots_info},and{restaurants_list}"
            f"Generate a chatbot-like itinerary for the user within a budget in {user_query} INR. "
            f"Provide the response based on above data if no data is present pls contact admin message should be provided"
        )

        try:
            # Call Gemini API to generate the response
            gemini_response = genai.GenerativeModel("gemini-1.5-flash").generate_content(prompt)
            gemini_chatbot_response = gemini_response.text.strip()
            print(user_query)
            ChatHistory.objects.create(
                user_query=user_query,
                chatbot_response=gemini_chatbot_response,
            )

            # Update response data with the chatbot response
            response_data['chatbot_response'] = gemini_chatbot_response
                        # Retrieve the chat history
            chat_history = ChatHistory.objects.order_by("-timestamp").values(
                "user_query", "chatbot_response", "timestamp"
            )
            response_data.update(
                {
                    "rooms": rooms_list,
                    "rented_vehicles": vehicles_list,
                    "nearby_spots": {
                        "free_entry_spots": free_spots_list,
                        "paid_spots": paid_spots_info,
                    },
                    "restaurants": restaurants_list,
                    "chatbot_response": gemini_chatbot_response,
                    "chat_history": list(chat_history),
                }
            )

            



            # Return the chatbot-like response with the itinerary data
            return Response(response_data, status=200)
        
        except Exception as e:
            return Response({"error": str(e)}, status=400)