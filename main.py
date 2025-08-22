import langchain_helper as lch
import document_scraping as dosp

def doc_version():
    print(" $$$ Great! Make sure that the file you want is in the same folder as this file (main.py) $$$")
    doc_type = input("Can you tell me the name of the file you want to summarize [type the file name exactly and include the file type, ie... requirements.txt: ")
    text = dosp.get_text(doc_type)
    while(True):
        if(text == "Invalid File Type"):
            print("$$$ Sorry but that is an incompatible file type! Try again")
            doc_type = input("Can you tell me the name of the file you want to summarize [type the file name exactly and include the file type, ie... requirements.txt: ")
            text = dosp.get_text(doc_type)
            continue
        else:
            break
    
    while(True):
        summary_length = input("$$$ How long would you like the summary to be [type SHORT|MEDIUM|LONG]: ")
        if (summary_length == "SHORT" or summary_length == "MEDIUM" or summary_length == "LONG"):
            break
        else:
            print("$$$ Invalid option. Try again!")
            continue

    response = lch.prompt_template_loader(text, summary_length)
    print(" \n\n $$$ Here is your summary: \n\n ")

    return response


def text_version():
    text = input("$$$ Great! Can you insert the text here: ")
    while(True):
        summary_length = input("$$$ How long would you like the summary to be [type SHORT|MEDIUM|LONG]: ")
        if (summary_length == "SHORT" or summary_length == "MEDIUM" or summary_length == "LONG"):
            break
        else:
            print("$$$ Invalid option. Try again!")
            continue
            
    print("\n$$$ Summarizing... $$$ \n\n")
    response = lch.prompt_template_loader(text, summary_length)
    print(" \n\n $$$ Here is your summary: \n\n ")

    return response
    

def main():
    while(True):
        doctype_option = input("$$$ Are you inserting text [type TEXT] or do you want to select a file [type DOC] (note only one file can be used at a time). Type EXIT, to quit: ")
        if(doctype_option == "TEXT"):
            summary_report = text_version()
            print(summary_report)
            break
        elif (doctype_option == "DOC"):
            summary_report = doc_version()
            print(summary_report)
            break
        elif (doctype_option == "EXIT"):
            return
        else:
            print("$$$ Invalid option. Try again!")
            continue

    while(True):
        qa_loop_request = input("$$$ Hope you enjoyed your summary! Do you want to start a Q/A session? [Y/N]: ")
        if (qa_loop_request == "y" or qa_loop_request == "Y"):
            while(qa_loop_request != "n" or qa_loop_request != "N"):
                question = input("$$$ Please ask a question about the summary [You can also type EXIT to leave this mode]: ")
                if question == 'EXIT':
                    break
                else:
                    answer_result = lch.question_and_answers_responder(question, summary_report)
                    print("$$$ Processing question... $$$ \n\n")
                    print("$$$ Here is the answer to your question $$$ \n")
                    print(answer_result)
                    qa_loop_request = input("$$$ Hope that helped! Would you like to ask another question? [Y/N]:")
            break
        elif(qa_loop_request == "n" or qa_loop_request == "N"):
            print("$$$ Bye-Bye!")
            break
        else:
            print("$$$ Invalid option. Try again!")
            continue

if __name__ == "__main__":
    main()