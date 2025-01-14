FROM python:3.11

# set the current working directory to "/code"
WORKDIR /code

# copy the file with the requirements to the "/code" directory
COPY ./requirements.txt /code/requirements.txt

# install the package dependencies in the requirements.txt file
RUN pip install --no-cache-dir --upgrade -r requirements.txt
RUN python -m spacy download en_core_web_sm

# copy the model, tokenizer and classifier class to the "/code" directory
COPY ./Index_Query_Text.py /code/Index_Query_Text.py

# copy the app directory inside the /code directory
COPY ./main.py /code/main.py


# set the command to run the uvicorn server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]