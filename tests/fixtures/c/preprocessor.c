#ifndef HEADER_H
#define HEADER_H

#define MAX(a, b) ((a) > (b) ? (a) : (b))
#define VERSION 1

#ifdef DEBUG
    #define LOG(msg) printf("%s\n", msg)
#else
    #define LOG(msg)
#endif

#pragma once

#endif