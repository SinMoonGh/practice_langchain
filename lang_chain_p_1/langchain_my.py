# main.py
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chat_models import ChatOpenAI
from langchain.schema import ChatMessage
import streamlit as st
from dotenv import load_dotenv
import os

# main.py 시작하는 파일

# .env 파일에서 환경 변수를 로드합니다.
load_dotenv()

# 환경 변수를 사용하여 API 키를 불러옵니다.
openai_api_key = os.getenv('NEW_API_KEY')

API_KEY = openai_api_key
MODEL = "gpt-3.5-turbo"

class StreamHandler(BaseCallbackHandler):
    def __init__(self, container, initial_text=""):
        self.container = container
        self.text = initial_text

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.text += token
        self.container.markdown(self.text)

want_to = """너는 아래 내용을 기반으로 질의응답을 하는 로봇이야.
content
{}
"""

content="""
1. Classic Espresso Martini:
Combine the rich flavors of coffee and vodka in this classic cocktail. Mix espresso, vodka, coffee liqueur, and simple syrup in a shaker with ice. Shake vigorously and strain into a martini glass. Garnish with coffee beans for an elegant touch.
 
 
2. Iced Vanilla Latte:
For a refreshing twist on a latte, try this iced version. Brew a strong cup of coffee or espresso, add vanilla syrup and milk, and stir well. Pour over ice and enjoy the smooth and creamy flavors of this chilled delight.
 
 
3. Mocha Frappuccino:
Indulge in a homemade version of the popular mocha frappuccino. Blend coffee, milk, chocolate syrup, sugar, and ice until smooth and frothy. Top with whipped cream and a drizzle of chocolate sauce for a decadent treat.
 
 
4. Caramel Macchiato:
Create your own caramel macchiato by combining espresso, steamed milk, and caramel syrup. Top with a dollop of foamed milk and a drizzle of caramel sauce. Savor the delightful combination of sweet caramel and rich coffee.
 
 
5. Vietnamese Iced Coffee:
Experience the bold flavors of Vietnamese coffee by combining strong brewed coffee with sweetened condensed milk. Pour the mixture over ice and enjoy the unique and irresistible taste of this beloved beverage.
 
 
6. Pumpkin Spice Latte:
Embrace the flavors of fall with a homemade pumpkin spice latte. Brew a cup of coffee or espresso, add pumpkin puree, pumpkin spice mix, sweetener, and milk. Stir well and top with whipped cream and a sprinkle of cinnamon for a cozy and seasonal delight.
 
 
7. Affogato:
Indulge in the simplicity of an affogato, a delightful combination of espresso and ice cream. Brew a shot of espresso and pour it over a scoop of your favorite ice cream. Witness the magic as the hot espresso melts the ice cream, creating a delightful fusion of flavors.
 
 
8. Honey Cinnamon Latte:
Add warmth and sweetness to your latte with the combination of honey and cinnamon. Brew a cup of coffee or espresso, add honey and a sprinkle of cinnamon, and stir well. Top with frothed milk for a comforting and aromatic experience.
 
 
9. Salted Caramel Cold Brew:
Elevate your cold brew experience with a touch of salted caramel. Brew cold brew coffee, add caramel syrup and a pinch of sea salt, and stir well. Serve over ice and enjoy the contrasting flavors of sweet caramel and salty undertones.
 
 
10. Irish Coffee:
Experience the perfect blend of coffee and whiskey in an Irish coffee. Brew a cup of strong coffee, add a shot of Irish whiskey, sweeten with sugar if desired, and top with whipped cream. Sip slowly and savor the harmonious combination of flavors.
"""

st.header("")
st.info("안녕하세요. 커피 레시피를 알려줍니다. 편하게 물어보세요.")

if "messages" not in st.session_state:
    st.session_state["messages"] = [ChatMessage(role="assistant", content="안녕하세요! 커피의 레시피를 물어봐 입니다.")]

for msg in st.session_state.messages:
    st.chat_message(msg.role).write(msg.content)

if prompt := st.chat_input():
    st.session_state.messages.append(ChatMessage(role="user", content=prompt))
    st.chat_message("user").write(prompt)

    if not API_KEY:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    with st.chat_message("assistant"):
        stream_handler = StreamHandler(st.empty())
        llm = ChatOpenAI(openai_api_key=API_KEY, streaming=True, callbacks=[stream_handler], model_name=MODEL)
        response = llm([ ChatMessage(role="system", content=want_to.format(content))]+st.session_state.messages)
        st.session_state.messages.append(ChatMessage(role="assistant", content=response.content))