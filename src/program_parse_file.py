

import argparse
from pathlib import Path
import traceback, sys
# import json, re
from datetime import datetime, timezone
import codecs
import io





if __name__ == '__main__':
    # run as a program
    from lib.mdd_parser import parse
elif '.' in __name__:
    # package
    from .lib.mdd_parser import parse
else:
    # included with no parent package
    from lib.mdd_parser import parse






def program_parse_file(config):
    try:
        time_start = datetime.now()
        parser = argparse.ArgumentParser(
            description="Parse MDD Metadata",
            prog='mdmtoolsapram mdd_parse'
        )
        parser.add_argument(
            '-1',
            '--file',
            help='Input file',
            type=str,
            required=True
        )
        # parser.add_argument(
        #     '--config-something',
        #     help='Config: some config',
        #     type=str,
        #     choices = ["somethinga","somethingb"],
        #     required=False
        # )
        args = None
        args_rest = None
        if( ('arglist_strict' in config) and (not config['arglist_strict']) ):
            args, args_rest = parser.parse_known_args()
        else:
            args = parser.parse_args()
        input_file = None
        if args.file:
            input_file = Path(args.file)
            input_file = '{input_file}'.format(input_file=input_file.resolve())
        else:
            raise FileNotFoundError('Inp source: file not provided; please use --file')

        if not(Path(input_file).is_file()):
            raise FileNotFoundError('file not found: {fname}'.format(fname=input_file))


        config = {
        }
        # if args.config_something:
        #     config['xxx'] = yyy

        print('MDM parse script: script started at {dt}'.format(dt=time_start))

        # with open(input_file,'r',encoding='utf-8') as f:
        bom = None
        bom_len = 0
        with open(input_file,'rb') as f:
            starting_bytes = f.read(4)
            for candidate in (
                codecs.BOM_UTF8,
                codecs.BOM_UTF16_LE,
                codecs.BOM_UTF16_BE,
                codecs.BOM_UTF32_LE,
                codecs.BOM_UTF32_BE,
            ):
                if starting_bytes.startswith(candidate):
                    bom = candidate
                    bom_len = len(bom)
                    break
            encoding_map = {
                codecs.BOM_UTF8: 'utf-8-sig',
                codecs.BOM_UTF16_LE: 'utf-16-le',
                codecs.BOM_UTF16_BE: 'utf-16-be',
                codecs.BOM_UTF32_LE: 'utf-32-le',
                codecs.BOM_UTF32_BE: 'utf-32-be',
            }
            encoding = encoding_map.get(bom, 'utf-8')
        
        with open(input_file, 'rb') as f_in:

            f_in.seek(bom_len)

            f = io.TextIOWrapper(f_in, encoding=encoding)

            print('MDM parse script: reading input file...')
            txt = f.read()

            print('MDM parse script: calling parser...')
            result = parse(txt)

            print('MDM parse script: finished')

        time_finish = datetime.now()
        print('MDM parse script: finished at {dt} (elapsed {duration})'.format(dt=time_finish,duration=time_finish-time_start))
    except Exception as e:
        # for pretty-printing any issues that happened during runtime; if we hit FileNotFound I don't appreciate when a log traceback is shown, the error should be simple and clear
        # the program is designed to be user-friendly
        # that's why we reformat error messages a little bit
        # stack trace is still printed (I even made it longer to 20 steps!)
        # but the error message itself is separated and printed as the last message again

        # for example, I don't write 'print('File Not Found!');exit(1);', I just write 'raise FileNotFoundErro()'
        print('',file=sys.stderr)
        print('Stack trace:',file=sys.stderr)
        print('',file=sys.stderr)
        traceback.print_exception(e,limit=20)
        print('',file=sys.stderr)
        print('',file=sys.stderr)
        print('',file=sys.stderr)
        print('Error:',file=sys.stderr)
        print('',file=sys.stderr)
        print('{e}'.format(e=e),file=sys.stderr)
        print('',file=sys.stderr)
        exit(1)

