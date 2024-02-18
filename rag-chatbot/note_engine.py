from llama_index.core.tools import FunctionTool
import os
from definitions import ROOT_DIR

note_file = os.path.join(ROOT_DIR, "rag-chatbot", "data", "notes.txt")


def save_note(note):
    """
    This function will upend a note to a txt file in the provided path.
    """
    if not os.path.exists(note_file):
        open(note_file, "w")

    with open(note_file, "a") as f:
        f.writelines([note + "\n"])

    return "note saved"


# A note_saver tool that the agent is able to use in order to upend notes to a text file
note_engine = FunctionTool.from_defaults(
    fn=save_note,
    name="note_saver",
    description="This tool can save a text based note to a file for the user. It should only be used when the user explicitly asks to save a note.",
)
