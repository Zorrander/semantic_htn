FROM python-with-cobowl

ADD /semantic_htn /semantic_htn/semantic_htn
ADD /tests /semantic_htn/tests
ADD setup.py /semantic_htn

WORKDIR /semantic_htn

RUN python -m pip install .

# Specify the application startup script
CMD python -m unittest tests/compound_task_test.py
