#!/bin/bash
export TESTBOT=$(dirname ${BASH_SOURCE[@]} | sed -e 's|/bin$|/|')

if [ -e $TESTBOT/lib ]
then
    [[ -z "$PYTHONPATH" ]] && PYTHONPATH=$TESTBOT/lib \
        || PYTHONPATH=$TESTBOT/lib:$PYTHONPATH
    export PYTHONPATH
elif [ -e $TESTBOT/testbot ]
then
    [[ -z "$PYTHONPATH" ]] && PYTHONPATH=$TESTBOT \
        || PYTHONPATH=$TESTBOT:$PYTHONPATH
    export PYTHONPATH
else
    echo "Error: No known location for testbot."
    echo "  Either run directly from the git repository"
    echo "    git clone https://github.com/mlouhivu/test-bot.git"
    echo "    test-bot/bin/bot"
    echo "  or install first (pip install)"
fi
