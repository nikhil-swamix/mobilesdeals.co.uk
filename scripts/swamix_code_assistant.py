import glob, os, hashlib, base64, chromadb
from openai import OpenAI
import chromadb.utils.embedding_functions as embedding_functions
import chromadb, base64

client = chromadb.PersistentClient(
    path="chroma.db",
)
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key=os.getenv("OPENAI_API_KEY"), model_name="text-embedding-3-small"
)


def b64e(s):
    return base64.b64encode(s.encode()).decode("utf-8")


def b64d(s):
    return base64.b64decode(s.encode()).decode("utf-8")


def sha256(content):
    return hashlib.sha256(content.encode()).hexdigest()


def get_files(directory='src', extensions=[".svelte", '.js']):
    file_paths = []
    for ext in extensions:
        file_paths.extend(glob.glob(f'{directory}/**/*{ext}', recursive=True))
    return file_paths


def attach_summary_ai(file_path, content):
    summary = (
        CLIENT.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "user", "content": content},
                {
                    "role": "system",
                    "content": f"""
                    1. this is a code file whose path is {file_path} try to include in beginning, 
                    2. explain only technical aspects of code, be as precise as possible, emphasing on logic, rather than content.""",
                },
            ],
            n=1,
            top_p=0.2,
        )
        .choices[0]
        .message.content
    )
    print(f"AI: created summary for {file_path}")
    if file_path.endswith('.svelte'):
        content = f"<!-- {summary} -->" + content

    if file_path.endswith('.js'):
        content = f"/* {summary} */" + content

    return content


def index_code(files=[], smart=True, dump=True):
    """
    Merge code from a list of files into a single file named 'codebase.txt'.
    :param files: A list of file paths to merge.
    """
    if smart:
        files = get_files("../src")
    with open('codebase.txt', 'w+') as cfile:
        for file_path in files:
            if dump:
                with open(file_path, 'r') as file:
                    contents = file.read()
                    print(file_path)
                    cfile.write(f'\n[---------- {file_path} ----------]\n')
                    cfile.write(contents)
            else:
                fcontents = open(file_path).read()
                pass
                # db.insert({'hash': sha256(fcontents) }, doc_id=b64e(file_path))


# 3mnhfz7UR2a5LtE8
def chromify():

    collection = client.create_collection("codebase", get_or_create=True, embedding_function=openai_ef)

    for file_path in get_files(directory='../src'):
        contents = open(file_path, 'r').read()
        fid = b64e(file_path)
        chash = sha256(contents)
        docexists = collection.get(ids=[file_path])
        contents = contents.replace('\t', '')

        if len(contents) <= 1:
            print(f"Skipping:Empty: {file_path}")
            continue

        if len(docexists['ids']) == 0:
            contents = attach_summary_ai(file_path, contents)
            print(f"Adding {file_path}")
            collection.add(
                documents=[contents],
                ids=[file_path],
                metadatas=[{"hash": chash}],
            )

        if len(docexists['ids']) > 0 and docexists['metadatas'][0]['hash'] != chash:
            print(f"Updating {file_path}")
            contents = attach_summary_ai(file_path, contents)
            collection.update(
                documents=[contents],
                ids=[file_path],
                metadatas=[{"hash": chash}],
            )


def vsearch(query, collection='codebase', results=3):
    import chromadb, base64

    collection = client.get_or_create_collection(name=collection, embedding_function=openai_ef)
    q = collection.query(
        query_texts=[query],
        n_results=results,
        # include=["data"],
        # where={"metadata_field": "is_equal_to_this"}, # optional filter
        # where_document={"$contains":"search_string"}  # optional filter
    )
    r = ""
    for i, c in zip(q['ids'][0], q['documents'][0]):
        r += f">>>{i}:\n{c}\n\n"

    # print(r)
    return r


if __name__ == "__main__":
    CLIENT = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    MODEL = "gpt-4-0125-preview"
    # merge_code()
    # codebase = open('codebase.txt').read()
    # index_code()
    chromify()

    QUERY = "complete the shadow filters store, since clicking on navbar-DistinctDropdown its not updating the compare page"
    context = vsearch(QUERY, results=5)
    ai_resp = CLIENT.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "user", "content": "im giving you context: " + context},
            {
                "role": "user",
                "content": """IMPORTANT: 
            1. give only code markdown blocks i need to write whole code! in backticks and also its path
            2. for example ```javascript:filepath 
            3. no comments required as im a professional developer on strict timeline. 
            4. no heading or trailing messages or explanations.
            5. make very beautiful styling, try tu use shadcn components, tailwindcss, sveltekit etc.
            6. we are already using https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.2/css/bootstrap.min.css | fontawesome 6""",
            },
            {"role": "user", "content": "QUESTION: " + QUERY},
            # {"role": "system", "content": "i have understood your query and you are looking for a detailed copy pastable code, just a minute let me generate it for you."},
        ],
        n=1,
        top_p=0.5,
        max_tokens=4096,
        # response_format={"type": "json_object"},
        # stream=True,
    )
    print(ai_resp.choices[0].message.content)
