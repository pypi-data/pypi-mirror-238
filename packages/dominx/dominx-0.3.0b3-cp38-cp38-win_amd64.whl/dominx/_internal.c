#include "_internal.h"

void
stringf(char **out, const char *format, ...)
{
    va_list args;
    va_start(args, format);

    // Determine the size required for the formatted string
    int size = vsnprintf(NULL, 0, format, args);
    if (size < 0) {
        // Handle vsnprintf error
        *out = NULL;
        va_end(args);
        return;
    }

    // Allocate memory for the formatted string
    *out = (char *)malloc(size + 1);
    if (*out != NULL) {
        // Reset va_list and format into the allocated memory
        va_end(args);
        va_start(args, format);
        int result = vsnprintf(*out, size + 1, format, args);
        if (result < 0) {
            // Handle vsnprintf error after allocating memory
            free(*out);
            *out = NULL;
        }
    }

    va_end(args);
}
