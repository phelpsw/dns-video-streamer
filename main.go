package main

import (
    "net"
    "fmt"
    "encoding/base64"
    "encoding/binary"
    "strconv"
)


func query_worker(id int, segments <-chan string, results chan<- string) {
    for segment := range segments {
        // TODO Add timeout logic
        // TODO Add retry on failure logic, prioritize lower indicies so they
        // get retried asap
        val, err := net.LookupTXT(segment)
        if err != nil {
            fmt.Printf("Could not lookup segment %v\n", segment)
            continue
        }
        fmt.Printf("Worker %v received segment %v -> %v\n", id, segment, val)
        results <- segment
    }
}

func main() {
    zone := "movies.zzyzxgazette.xyz"
    val, err := net.LookupTXT("manifest." + zone)
    if err != nil {
        fmt.Printf("Could not find manifest.%v", zone)
        return
    }
    if len(val) != 1 {
        fmt.Println("Unexpected length")
        return
    }
    header_b64 := []byte(val[0])
    header_buf := make([]byte, len(header_b64))
    num, err := base64.StdEncoding.Decode(header_buf, header_b64)
    if err != nil {
        fmt.Println("error:", err)
        return
    }
    if num != 4 {
        fmt.Println("Unexpected header size %v", num)
        return
    }
    num_segments := binary.BigEndian.Uint32(header_buf)
    fmt.Printf("%v segments in stream\n", num_segments)

    worker_count := 100
    // TODO: channel_size equal to the number of segments isn't reasonable,
    // needs to be a small number.
    channel_size := num_segments
    segments := make(chan string, channel_size)
    results := make(chan string, channel_size)
    for worker := 0; worker < worker_count; worker++ {
        go query_worker(worker, segments, results)
    }

    for j := 0; j < int(num_segments); j++ {
        segments <- strconv.Itoa(j) + "." + zone
    }
    close(segments)

    for a := 0; a < int(num_segments); a++ {
        <-results
    }

    // TODO Consumer channel reorders and writes to stream.  If segment has
    // been attempted a certain number of times, it will skip that segment and
    // forge ahead in writing to output
}




