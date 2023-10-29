function(link_to_target targetName)
    vcpkg_download(miniz)
    find_package(miniz CONFIG REQUIRED)
    target_link_libraries(${targetName} PRIVATE miniz::miniz)
endfunction()