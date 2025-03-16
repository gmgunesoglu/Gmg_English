import {Component, Input, Output, EventEmitter, ViewChild} from '@angular/core';
import {TextDetail} from "../../../models/text-detail";
import {UpdateText} from "../../../models/update-text";
import {ReadingService} from "../../../services/reading.service";
import {FormBuilder, FormControl, FormGroup, Validators} from "@angular/forms";

@Component({
  selector: 'app-text',
  templateUrl: './text.component.html',
  styleUrls: ['./text.component.scss']
})
export class TextComponent {
  @Input() text_detail!: TextDetail;
  @Input() unit_id!: number;
  @Output() back = new EventEmitter<void>();
  is_updating_text: boolean = false;
  update_text!: UpdateText;
  titlePattern = '^(?!\\s*$).+';

  constructor(
    private readingService: ReadingService,

  ) {
  }

  ngOnInit(): void {
    this.update_text = {
      unit_id: this.unit_id,
      context: "",
      title: "",
    }
  }

  closeText(): void {
    this.back.emit();
  }

  updateText() {
    this.update_text.title = this.text_detail.title;
    this.update_text.context = this.text_detail.context;
    this.is_updating_text = true;
  }

  cancelUpdateText() {
    this.is_updating_text = false;
  }

  saveUpdateText() {
    this.readingService.updateText(this.update_text, this.text_detail.id).subscribe(
      (result) => {
        console.log(result)
      },
      (error) => {
        alert(error.error);
        console.log(error);
      }
    );
    this.is_updating_text = false;
  }
}
