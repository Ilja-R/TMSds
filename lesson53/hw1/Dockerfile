FROM python:3.12

ENV TO_GREET='Teach Me Skills'

WORKDIR /app

COPY . /app

ENTRYPOINT ["python"]
CMD ["greeting.py"]

# Build the image
# docker build -t robalkin-python:53 .

# Run the image
# docker run --rm robalkin-python:53 greeting.py
# docker run --rm -e TO_GREET="Students" robalkin-python:53 greeting.py
# docker run --rm robalkin-python:53 sum_numbers.py 100 2.5
# docker run --rm robalkin-python:53 sum_numbers.py 100
