import os.path
import subprocess


def convert_gif_to_png(upload_dir, filename):
    filepath = os.path.join(upload_dir, filename)
    p = subprocess.Popen(['identify', '-format', '%s %T\n', filepath],
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()

    delays = []
    images_count = 0
    for line in out.split('\n'):
        if line.strip() != '':
            images_count += 1
            delay = line.split()[1]
            if int(delay) == 0:
                delay = '1'
            delays.append(delay)

    name = os.path.basename(filepath)[0:-4]
    name = name.lower()
    for c in "_-. ":
        name = name.replace(c,'')

    if all(map(lambda x: x == delays[0], delays)):
        delays_str = delays[0]
    else:
        delays_str = '-'.join(delays)

    out_filename = "%s.%s-%s.png" % (name, images_count, delays_str)

    cmd = ['convert', '-coalesce', filepath, '%03d.png',
             '+append', os.path.join(upload_dir, out_filename)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()

    return out_filename

