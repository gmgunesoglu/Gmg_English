import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Unit } from "../models/unit";
import { TextDetail } from "../models/text-detail";
import {Observable} from "rxjs";
import {CreateUnit} from "../models/create-unit";
import {CreateText} from "../models/create-text";
import {CreatedText} from "../models/created-text";

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

  getTextDetail(titleId: number) {
    return this.http.get<TextDetail>(this.url + "texts/" + titleId);
  }

  createUnit(create_unit: CreateUnit) {
    return this.http.post<Unit>('http://localhost:8000/readings/units', create_unit);
  }

  deleteText(id: number) {
    return this.http.delete<string>(`http://localhost:8000/readings/texts/${id}`);
  }

  deleteUnit(id: number) {
    return this.http.delete<string>(`http://localhost:8000/readings/units/${id}`);
  }

  createText(createText: CreateText) {
    return this.http.post<CreatedText>('http://localhost:8000/readings/texts', createText)
  }
}
