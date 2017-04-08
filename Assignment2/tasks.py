import os, json
from email.utils import formatdate
from ResponseBuilder import ResponseBuilder, build_generic_response


# Each task must close it's own connection
def task_handle_get(connection, file_name, user_agent, head_request):
    response_builder = ResponseBuilder()
    response_builder.with_date(formatdate(timeval=None, localtime=False, usegmt=True)) \
        .with_content_type("text/html; charset=utf-8") \
        .with_server("FredServer") \
        .with_user_agent(user_agent)

    try:
        file_path = os.getcwd() + "/text_files/" + file_name
        my_file = open(file_path)
        if not head_request:
            l = my_file.read(10)
        else:
            l = None
        response_builder.with_body(l) \
            .with_status(200) \
            .with_content_length(os.path.getsize(file_path)) \
            .with_status_en("OK")
        connection.send(response_builder.build())
        while l and not head_request:
            l = my_file.read(10)
            connection.send(l)
        my_file.close()
    except IOError:
        l = """
<html><body><h1>File Not Found</h1></body></html>
"""
        response_builder.with_body(l) \
            .with_status(404) \
            .with_status_en("File Not Found") \
            .with_content_length(0)

        connection.send(response_builder.build())
    finally:
        connection.close()


def task_handle_post_request(connection, message_body):
    body = json.loads(message_body)
    response = build_generic_response(200, "OK", None).build()
    try:
        connection.send(response)
    finally:
        connection.close()
