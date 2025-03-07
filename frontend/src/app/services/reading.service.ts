import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Unit } from "../models/unit";
import {Observable} from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class ReadingService {

  private url: string = "http://localhost:8000/readings/"

  constructor(
    private http: HttpClient
  ) { }


  getUnits(): Observable<Unit[]> {
    return this.http.get<Array<Unit>>(this.url + "units");
  }

}
