import sys
import shutil


PADDING = 4


def color_line(line, color_number):
    result = ''
    if color_number >= 8:
        result += "\033[1m"
        color_number -= 8
    result += f"\033[03{color_number}m{line}"
    # reset font:
    result += "\033[0m"
    return result


def bold_line(line):
    return f'\033[1m{line}\033[0m'


def get_term_width():
    return shutil.get_terminal_size((80, 80)).columns


def format_paragraph(line):
    term_width = get_term_width()
    max_line_width = term_width - PADDING * 2

    result = []
    current_line = []
    line_length = 0
    for word in line.split():
        if len(word) + line_length > max_line_width:
            result.append(current_line)
            current_line = []
            line_length = 0
        current_line.append(word)
        line_length += len(word) + 1
    result.append(current_line)

    return '\n'.join([
        ' '.join(
            [(PADDING-1)*' ', ] +
            words +
            [(PADDING-1)*' ', ],
        )
        for words in result
    ])


def print_not_found_packages(not_found_packages):
    print("{} {}".format(
        color_line(':: warning:', 11),
        bold_line('Following packages can not be found in AUR:'),
    ))
    for package in not_found_packages:
        print(format_paragraph(package))


def pretty_print_upgradeable(packages_updates):

    def get_common_string(str1, str2):
        result = ''
        counter = 0
        while str1[counter] == str2[counter]:
            result += str1[counter]
            counter += 1
        return result

    def pretty_format(pkg_update):
        common_version = get_common_string(
            pkg_update.current_version, pkg_update.aur_version
        )
        new_version_postfix = pkg_update.aur_version
        if common_version != '':
            new_version_postfix = pkg_update.aur_version.split(
                common_version
            )[1]
        version_color = 10
        old_color = 11
        new_color = 9
        column_width = min(int(get_term_width() / 2), 45)
        sort_by = '{:03d}{}'.format(
            len(common_version)*10+len(pkg_update.aur_version),
            pkg_update.pkg_name
        )
        return ' {:<{width}} {:<{width2}} -> {}{}'.format(
            bold_line(pkg_update.pkg_name),
            color_line(common_version, version_color) +
            color_line(
                pkg_update.current_version.split(common_version)[1]
                if common_version != ''
                else pkg_update.current_version,
                old_color
            ),
            color_line(common_version, version_color),
            color_line(new_version_postfix, new_color),
            width=column_width,
            width2=column_width - 3
        ), sort_by

    print(
        '\n'.join([
            f'{line}' for line, _ in sorted(
                [
                    # format_paragraph(pretty_format(pkg_update))
                    pretty_format(pkg_update)
                    for pkg_update in packages_updates
                ],
                key=lambda x: x[1],
                # reverse=True
            )
        ])
    )


def print_upgradeable(packages_updates):
    print('\n'.join([
        pkg_update.pkg_name
        for pkg_update in packages_updates
    ]))


def print_version():
    sys.stdout.buffer.write(r"""
      /:}               _
     /--1             / :}
    /   |           / `-/
   |  ,  --------  /   /
   |'                 Y
  /                   l     Pikaur v0.1
  l  /       \        l     (C) 2018 Pikaur development team
  j  ●   .   ●        l     Licensed under GPLv3
 { )  ._,.__,   , -.  {
  У    \  _/     ._/   \

""".encode())