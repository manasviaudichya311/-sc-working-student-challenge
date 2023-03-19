*** Settings ***
Library    RequestsLibrary


*** Test Cases ***
Asking for 'life;universe;everything' give us 42
    ${response}=    GET    http://server:80/answer    params=search=life;universe;everything    expected_status=200
    Should Be Equal As Strings    ${response.text}    42
    # Implement a proper test that will:
    # - Send a GET request to the server, on the resource `/answer`, with
    # the following value on the `search` parameter: life;universe;everything
    # - Ensure the server replied with 200 error code
    # - Ensure the server replied 42

Asking for something else give us unknown
    ${response}=    GET    http://server:80/answer    params=search=the truth    expected_status=404
    Should Be Equal As Strings    ${response.text}    unknown
    # Implement a proper test that will:
    # - Send a GET request to the server, on the resource `/answer`, with
    # the following value on the `search` parameter: the truth
    # - Ensure the server replied with 404 error code
    # - Ensure the server replied unknown
    # Note: You can also ask other things, but we don't think it will be able
    # to give a good answer.
