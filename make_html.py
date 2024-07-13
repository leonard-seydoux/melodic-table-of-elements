"""Produce the main HTML file for the website."""

import elements


class HTML:
    """Class to create an HTML file."""

    def __init__(self, header_filepath="snippets/header.html"):
        """Initialize the HTML file.

        The HTML file is created with a header.

        Arguments:
        ----------
        header_filepath : str
            The path to the header file.
        """
        self.html = open(header_filepath).read()

    def save(self, filename):
        """Save the HTML file.

        Append the footer to the HTML file and save it to a file.

        Arguments:
        ----------
        filename : str
            The name of the file to save the HTML content to.
        """
        self.append_footer()
        with open(filename, "w") as file:
            file.write(self.html)

    def append_table(self, table):
        """Append the HTML table to the HTML file.

        Arguments:
        ----------
        table : str
            The HTML table to append.
        """
        # Turn table into HTML
        table_html = table.to_html(
            header=False,
            index=False,
            na_rep="",
            justify="center",
            border="",
            escape=False,
        )

        # Make td class the name of the block span content
        table_html = stylize_table_html(table_html)

        # Append the table to the HTML file
        self.html += table_html

    def append_footer(self, footer_filepath="snippets/footer.html"):
        """Close the HTML file."""
        self.html += open(footer_filepath).read()


def stylize_table_html(html):
    """Change the class of the td element to the block name."""
    # Prepare the new HTML
    new_html = ""

    # Iterate over the lines of the HTML
    for line in html.split("\n"):
        if "<td>" in line:
            if "<span class='block'>" in line:

                # Get the block name
                block = line.split("<span class='block'>")[1].split("</span>")[
                    0
                ]

                # Get the atomic number
                atomic_number = line.split("<span class='number'>")[1].split(
                    "</span>"
                )[0]

                # Replace the td class and id
                line = line.replace(
                    "<td>", f"<td class='{block}' id='n{atomic_number}'>"
                )

        # Append the line to the new HTML
        new_html += line + "\n"

    return new_html


def create_cell(element):
    """Create the cell for the element."""
    return (
        "<span class='number'>"
        + str(element["atomic_number"])
        + "</span>"
        + "<span class='element'>"
        + element["name"]
        + "</span>"
        + element["symbol"]
        + "<span class='block'>"
        + element["block"]
        + "</span>"
    )


if __name__ == "__main__":

    # Create the main HTML file
    html = HTML()

    # Read the complete periodic table
    periodic_table = elements.read()
    periodic_table = elements.clean(periodic_table)
    periodic_table = elements.move_f_block(periodic_table)

    # Create cell
    periodic_table.insert(0, "cell", periodic_table.apply(create_cell, axis=1))

    # Obtain the main table
    periodic_table = elements.pivot(periodic_table)

    # Insert the HTML table
    html.append_table(periodic_table)

    # Close the main HTML file
    html.save("index.html")
