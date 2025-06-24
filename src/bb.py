import json
import time
import asyncio
import aiohttp

async def send_req_async(session, course_id, cookies, course_type, num):
    #Url with action
    url = "https://lti11bits.azurewebsites.net/bitsservices.php?action=log-answer"

    #Needeed headers only
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie': cookies,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
    }

    #Offset + number
    page_id = course_id + num

    #Page title
    page_title = f"Question {num}"

    quiz_id = ""
    quiz_type = ""
    answer = {}

    #Change payload according to type
    if course_type == "v":
        quiz_id = "quiz-matching-16"
        quiz_type = "matching"
        answer = {
            "value": [{"target": "quiz-matching-16-target", "drop": "quiz-matching-16-drag"}],
            "label": "",
            "try": 1
        }
    elif course_type == "g":
        quiz_id = "quiz-sa-n"
        quiz_type = "sa"
        answer = {"value":[{"id":"sa-quiz-sa-n-1","ua":""}]}
    elif course_type == "m":
        quiz_id = "quiz-mc-z"
        quiz_type = "mc"
        answer = {"value":"1","label":"A","try": 1}

    #Make payload
    payload_dict = {
        "quizID": quiz_id,
        "quizGroup": "default",
        "quizType": quiz_type,
        "status": "correct",
        "answer": answer,
        "userTime": 9999,
        "page": page_id,
        "pageTitle": page_title
    }

    #Send the data
    form_data = {'data': json.dumps(payload_dict)}

    try:
        print(f"Sending answer {num} (Page ID: {page_id})")
        async with session.post(url, data=form_data, headers=headers) as response:
            response_text = await response.text()
            print(f"Request successful! Status: {response.status}, Response: {response_text}")
            return True
    except Exception as e:
        print(f"Error for {page_title}: {e}")
        return False

async def send_async_requests(course_id, cookies, course_type, max_requests=500, max_concurrent=50):
    print(f"Starting {max_requests} async requests with {max_concurrent} concurrent connections...")
    
    start_time = time.time()
    successful = 0
    failed = 0
    
    connector = aiohttp.TCPConnector(limit=max_concurrent, limit_per_host=max_concurrent)
    timeout = aiohttp.ClientTimeout(total=30)
    
    #Send per work
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def limited_send_req(num):
            async with semaphore:
                return await send_req_async(session, course_id, cookies, course_type, num)
        
        tasks = [limited_send_req(num) for num in range(1, max_requests + 1)]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for result in results:
            if isinstance(result, Exception):
                failed += 1
            elif result:
                successful += 1
            else:
                failed += 1
    
    end_time = time.time()
    print(f"\nResults: {successful} successful, {failed} failed")
    print(f"Total time: {end_time - start_time:.2f} seconds")
    print(f"Average: {max_requests / (end_time - start_time):.2f} requests/second")

def user_insert(course, unit, course_type):
    #Courses indexed
    available_courses = {
    "a111v": 0, "a111g": 0, "a111m": 0, 
    "a112v": 0, "a112g": 0, "a112m": 0, 
    "a113v": 0, "a113g": 0, "a113m": 0, 
    "a114v": 0, "a114g": 0, "a114m": 0, 
    "a115v": 0, "a115g": 0, "a115m": 0, 
    "a116v": 0, "a116g": 0, "a116m": 0, 
    "a117v": 0, "a117g": 0, "a117m": 0, 
    "a118v": 0, "a118g": 0, "a118m": 0, 
    "a121v": 0, "a121g": 0, "a121m": 0, 
    "a122v": 0, "a122g": 0, "a122m": 0, 
    "a123v": 0, "a123g": 0, "a123m": 0, 
    "a124v": 0, "a124g": 0, "a124m": 0, 
    "a125v": 0, "a125g": 0, "a125m": 0, 
    "a126v": 0, "a126g": 0, "a126m": 0, 
    "a127v": 0, "a127g": 0, "a127m": 0, 
    "a128v": 0, "a128g": 0, "a128m": 0, 
    "a211v": 0, "a211g": 0, "a211m": 0, 
    "a212v": 0, "a212g": 0, "a212m": 0, 
    "a213v": 0, "a213g": 0, "a213m": 0, 
    "a214v": 0, "a214g": 0, "a214m": 0, 
    "a215v": 0, "a215g": 0, "a215m": 0, 
    "a216v": 0, "a216g": 0, "a216m": 0, 
    "a217v": 0, "a217g": 0, "a217m": 0, 
    "a218v": 0, "a218g": 0, "a218m": 0, 
    "a221v": 0, "a221g": 0, "a221m": 0, 
    "a222v": 0, "a222g": 0, "a222m": 0, 
    "a223v": 0, "a223g": 0, "a223m": 0, 
    "a224v": 0, "a224g": 0, "a224m": 0, 
    "a225v": 0, "a225g": 0, "a225m": 0, 
    "a226v": 0, "a226g": 0, "a226m": 0, 
    "a227v": 0, "a227g": 0, "a227m": 0, 
    "a228v": 0, "a228g": 0, "a228m": 0, 
    "b111v": 0, "b111g": 0, "b111m": 0, 
    "b112v": 0, "b112g": 0, "b112m": 0, 
    "b113v": 0, "b113g": 0, "b113m": 0, 
    "b114v": 0, "b114g": 0, "b114m": 0, 
    "b115v": 0, "b115g": 0, "b115m": 0, 
    "b116v": 0, "b116g": 0, "b116m": 0, 
    "b117v": 0, "b117g": 0, "b117m": 0, 
    "b118v": 0, "b118g": 0, "b118m": 0, 
    "b121v": 0, "b121g": 0, "b121m": 0, 
    "b122v": 0, "b122g": 0, "b122m": 0, 
    "b123v": 0, "b123g": 0, "b123m": 0, 
    "b124v": 0, "b124g": 0, "b124m": 0, 
    "b125v": 0, "b125g": 0, "b125m": 0, 
    "b126v": 0, "b126g": 0, "b126m": 0, 
    "b127v": 0, "b127g": 0, "b127m": 0, 
    "b128v": 0, "b128g": 71712, "b128m": 71212, #b128g and m need number 1 id
    "b211v": 0, "b211g": 0, "b211m": 0, 
    "b212v": 0, "b212g": 0, "b212m": 0, 
    "b213v": 0, "b213g": 0, "b213m": 0, 
    "b214v": 0, "b214g": 0, "b214m": 0, 
    "b215v": 0, "b215g": 0, "b215m": 0, 
    "b216v": 0, "b216g": 0, "b216m": 0, 
    "b217v": 0, "b217g": 0, "b217m": 0, 
    "b218v": 0, "b218g": 0, "b218m": 0, 
    "b221v": 0, "b221g": 0, "b221m": 0, 
    "b222v": 0, "b222g": 0, "b222m": 0, 
    "b223v": 0, "b223g": 0, "b223m": 0, 
    "b224v": 0, "b224g": 0, "b224m": 0, 
    "b225v": 0, "b225g": 0, "b225m": 0, 
    "b226v": 0, "b226g": 0, "b226m": 0, 
    "b227v": 0, "b227g": 0, "b227m": 0, 
    "b228v": 0, "b228g": 0, "b228m": 0, 
    "c111v": 0, "c111g": 0, "c111m": 0, 
    "c112v": 0, "c112g": 0, "c112m": 0, 
    "c113v": 0, "c113g": 0, "c113m": 0, 
    "c114v": 0, "c114g": 0, "c114m": 0, 
    "c115v": 0, "c115g": 0, "c115m": 0, 
    "c116v": 0, "c116g": 0, "c116m": 0, 
    "c117v": 0, "c117g": 0, "c117m": 0, 
    "c118v": 0, "c118g": 0, "c118m": 0, 
    "c121v": 0, "c121g": 0, "c121m": 0, 
    "c122v": 0, "c122g": 0, "c122m": 0, 
    "c123v": 0, "c123g": 0, "c123m": 0, 
    "c124v": 0, "c124g": 0, "c124m": 0, 
    "c125v": 0, "c125g": 0, "c125m": 0, 
    "c126v": 0, "c126g": 0, "c126m": 0, 
    "c127v": 0, "c127g": 0, "c127m": 0, 
    "c128v": 0, "c128g": 0, "c128m": 0, 
    "c211v": 73376, "c211g": 0, "c211m": 0, 
    "c212v": 73424, "c212g": 0, "c212m": 0, 
    "c213v": 73015, "c213g": 73400, "c213m": 73400, #c213: 999, 200, 200 (just run g is enough)
    "c214v": 73076, "c214g": 73454, "c214m": 73455, #c214: 500, 500, 500 (just run g is enough)
    "c215v": 73760, "c215g": 73535, "c215m": 73660, #c215: 25, 100, 250
    "c216v": 73211, "c216g": 73618, "c216m": 73865, #c216: 500, 10, 10
    "c217v": 73272, "c217g": 73644, "c217m": 73670, #c217: 800, 20, 30
    "c218v": 73333, "c218g": 73872, "c218m": 73955, #c218: 300, 10, 10
    "c221v": 75144, "c221g": 75164, "c221m": 75164, #c221: 20, 1200, n #case c221g 75xxx jumps to 76xxx (TODO: Put special case so we don't accidentally DDOS ts) (just run g is enough)
    "c222v": 75474, "c222g": 76194, "c222m": 76194, #c222: 20, 100, 100 (just run g is enough)
    "c223v": 75583, "c223g": 76207, "c223m": 76207, #c223: 20, 200, 200 (just run g is enough)
    "c224v": 75526, "c224g": 76220, "c224m": 76220, #c224: 20, 100, 100 (just run g is enough)
    "c225v": 75630, "c225g": 76233, "c225m": 72633, #c225: 20, 100, 100 (just run g is enough)
    "c226v": 75678, "c226g": 76246, "c226m": 76246, #c226: 20, 100, 100 (just run g is enough)
    "c227v": 75835, "c227g": 76259, "c227m": 76259, #c227: 20, 100, 100 (just run g is enough)
    "c228v": 75883, "c228g": 76272, "c228m": 76272  #c228: 20, 100, 100 (just run g is enough)
    }

    #Amount of runs needed indexed
    run_times = {
    "a111v": 0, "a111g": 0, "a111m": 0, 
    "a112v": 0, "a112g": 0, "a112m": 0, 
    "a113v": 0, "a113g": 0, "a113m": 0, 
    "a114v": 0, "a114g": 0, "a114m": 0, 
    "a115v": 0, "a115g": 0, "a115m": 0, 
    "a116v": 0, "a116g": 0, "a116m": 0, 
    "a117v": 0, "a117g": 0, "a117m": 0, 
    "a118v": 0, "a118g": 0, "a118m": 0, 
    "a121v": 0, "a121g": 0, "a121m": 0, 
    "a122v": 0, "a122g": 0, "a122m": 0, 
    "a123v": 0, "a123g": 0, "a123m": 0, 
    "a124v": 0, "a124g": 0, "a124m": 0, 
    "a125v": 0, "a125g": 0, "a125m": 0, 
    "a126v": 0, "a126g": 0, "a126m": 0, 
    "a127v": 0, "a127g": 0, "a127m": 0, 
    "a128v": 0, "a128g": 0, "a128m": 0, 
    "a211v": 0, "a211g": 0, "a211m": 0, 
    "a212v": 0, "a212g": 0, "a212m": 0, 
    "a213v": 0, "a213g": 0, "a213m": 0, 
    "a214v": 0, "a214g": 0, "a214m": 0, 
    "a215v": 0, "a215g": 0, "a215m": 0, 
    "a216v": 0, "a216g": 0, "a216m": 0, 
    "a217v": 0, "a217g": 0, "a217m": 0, 
    "a218v": 0, "a218g": 0, "a218m": 0, 
    "a221v": 0, "a221g": 0, "a221m": 0, 
    "a222v": 0, "a222g": 0, "a222m": 0, 
    "a223v": 0, "a223g": 0, "a223m": 0, 
    "a224v": 0, "a224g": 0, "a224m": 0, 
    "a225v": 0, "a225g": 0, "a225m": 0, 
    "a226v": 0, "a226g": 0, "a226m": 0, 
    "a227v": 0, "a227g": 0, "a227m": 0, 
    "a228v": 0, "a228g": 0, "a228m": 0, 
    "b111v": 0, "b111g": 0, "b111m": 0, 
    "b112v": 0, "b112g": 0, "b112m": 0, 
    "b113v": 0, "b113g": 0, "b113m": 0, 
    "b114v": 0, "b114g": 0, "b114m": 0, 
    "b115v": 0, "b115g": 0, "b115m": 0, 
    "b116v": 0, "b116g": 0, "b116m": 0, 
    "b117v": 0, "b117g": 0, "b117m": 0, 
    "b118v": 0, "b118g": 0, "b118m": 0, 
    "b121v": 0, "b121g": 0, "b121m": 0, 
    "b122v": 0, "b122g": 0, "b122m": 0, 
    "b123v": 0, "b123g": 0, "b123m": 0, 
    "b124v": 0, "b124g": 0, "b124m": 0, 
    "b125v": 0, "b125g": 0, "b125m": 0, 
    "b126v": 0, "b126g": 0, "b126m": 0, 
    "b127v": 0, "b127g": 0, "b127m": 0, 
    "b128v": 0, "b128g": 200, "b128m": 200, #need to update request amount no exact amount tested
    "b211v": 0, "b211g": 0, "b211m": 0, 
    "b212v": 0, "b212g": 0, "b212m": 0, 
    "b213v": 0, "b213g": 0, "b213m": 0, 
    "b214v": 0, "b214g": 0, "b214m": 0, 
    "b215v": 0, "b215g": 0, "b215m": 0, 
    "b216v": 0, "b216g": 0, "b216m": 0, 
    "b217v": 0, "b217g": 0, "b217m": 0, 
    "b218v": 0, "b218g": 0, "b218m": 0, 
    "b221v": 0, "b221g": 0, "b221m": 0, 
    "b222v": 0, "b222g": 0, "b222m": 0, 
    "b223v": 0, "b223g": 0, "b223m": 0, 
    "b224v": 0, "b224g": 0, "b224m": 0, 
    "b225v": 0, "b225g": 0, "b225m": 0, 
    "b226v": 0, "b226g": 0, "b226m": 0, 
    "b227v": 0, "b227g": 0, "b227m": 0, 
    "b228v": 0, "b228g": 0, "b228m": 0, 
    "c111v": 0, "c111g": 0, "c111m": 0, 
    "c112v": 0, "c112g": 0, "c112m": 0, 
    "c113v": 0, "c113g": 0, "c113m": 0, 
    "c114v": 0, "c114g": 0, "c114m": 0, 
    "c115v": 0, "c115g": 0, "c115m": 0, 
    "c116v": 0, "c116g": 0, "c116m": 0, 
    "c117v": 0, "c117g": 0, "c117m": 0, 
    "c118v": 0, "c118g": 0, "c118m": 0, 
    "c121v": 0, "c121g": 0, "c121m": 0, 
    "c122v": 0, "c122g": 0, "c122m": 0, 
    "c123v": 0, "c123g": 0, "c123m": 0, 
    "c124v": 0, "c124g": 0, "c124m": 0, 
    "c125v": 0, "c125g": 0, "c125m": 0, 
    "c126v": 0, "c126g": 0, "c126m": 0, 
    "c127v": 0, "c127g": 0, "c127m": 0, 
    "c128v": 0, "c128g": 0, "c128m": 0, 
    "c211v": 200, "c211g": 0, "c211m": 0, #need to update request amount no exact amount tested
    "c212v": 200, "c212g": 0, "c212m": 0, #need to update request amount no exact amount tested
    "c213v": 999, "c213g": 200, "c213m": 200, #need to update request amount so we wont request too much
    "c214v": 500, "c214g": 500, "c214m": 500,
    "c215v": 25, "c215g": 100, "c215m": 250,
    "c216v": 500, "c216g": 10, "c216m": 10,
    "c217v": 800, "c217g": 20, "c217m": 30,
    "c218v": 300, "c218g": 10, "c218m": 10,
    "c221v": 20, "c221g": 1200, "c221m": 1200, #need to update request amount so we wont request too much
    "c222v": 20, "c222g": 100, "c222m": 100,
    "c223v": 20, "c223g": 200, "c223m": 200,
    "c224v": 20, "c224g": 100, "c224m": 100,
    "c225v": 20, "c225g": 100, "c225m": 100,
    "c226v": 20, "c226g": 100, "c226m": 100,
    "c227v": 20, "c227g": 100, "c227m": 100,
    "c228v": 20, "c228g": 100, "c228m": 100
    }

    #User input the course name
    course = input(f"Add course name (example: a11) (case sensitive): ")

    #User input the course unit
    while(unit > 8 or unit < 1):
        unit = int(input(f"Add course unit (1-8) (example: 1): "))
    unit = str(unit)

    #User input the course type 
    #Actually we can remove the (m) category, but just in case someone needs it
    print(f"\nCourse type:")
    print("Vocabulary (v)")
    print("Grammar (short answer) (g)")
    print("Grammar (multiple choice) (m)")
    while(course_type != "g" and course_type != "v" and course_type != "m"):
        course_type = input("Add course type first letter (v or g or m) (example: v): ").lower()

    #Get the course key
    get_key = course + unit + course_type

    #Get the page id
    course_id = available_courses[get_key]

    #Custom id if Bee decided to move it around, tbh just raise it in issues
    if course_id == 0:
        print("Course id not found")
        choice = input("Add custom id? (y/n)")
        if choice == "y":
            course_id = int(input("Add custom id: "))
        else:
            return
        
    #Cookies so they can track you
    cookies = input("Add your session cookie: ")

    #Req amount required already indexed
    req_amount = run_times[get_key];

    #Default 200 so this wont be a DDOS machine
    if req_amount == 0:
        req_amount = 200

    #Run the shit
    asyncio.run(send_async_requests(course_id, cookies, course_type, req_amount))

    #Automatically run m for convenience
    if course_type == "g":
        choice_key = course + unit + "m"
        choice_amnt = run_times[choice_key]
        if choice_amnt == 0:
            choice_amnt = 200
        asyncio.run(send_async_requests(course_id, cookies, "m", choice_amnt))

def menu():
    course = ""
    unit = 0
    course_type = ""

    #Just loops indefinitely till I want to explode
    while(1):
        print("IMPORTANT!! Running grammar task (g) will automatically run multiple choice task (m), so just running (g) is enough in most cases")
        user_insert(course, unit, course_type)
        opti = input(f"\nDo you want to do it for another course? (y/n)").lower()
        if opti != "y":
            break

menu()
print("Teto pear")