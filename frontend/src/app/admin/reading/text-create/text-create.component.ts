import {Component, EventEmitter, Input, Output} from '@angular/core';
import {Unit} from "../../../models/unit";
import {ReadingService} from "../../../services/reading.service";
import {CreatedText} from "../../../models/created-text";
import {CreateText} from "../../../models/create-text";


@Component({
  selector: 'app-text-create',
  templateUrl: './text-create.component.html',
  styleUrls: ['./text-create.component.scss']
})
export class TextCreateComponent {

  @Input() unit!: Unit;
  @Output() continueCreate: EventEmitter<CreatedText> = new EventEmitter<CreatedText>();
  @Output() cancelCreate: EventEmitter<void> = new EventEmitter<void>();
  create_text!: CreateText;

  constructor(
    private readingService: ReadingService
  ) {}

  ngOnInit() {
    console.log('Unit:', this.unit);
    this.create_text = {
      unit_id: this.unit.id,
      title: "",
      context: "",
    }
  }

  createNewText(): void {
    this.readingService.createText(this.create_text).subscribe(
      (created_text) => {
        this.continueCreate.emit(created_text);
      },
      (error) => {
        alert(error.error);
        console.log(error);
      }
    );
  }

  cancelCreateNewText() {
    this.cancelCreate.emit();
  }
}
