import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import {HttpClientModule} from "@angular/common/http";
import {FormsModule, ReactiveFormsModule} from "@angular/forms";
import {MinContextLengthDirective} from "./validators/min-context-length.directive";

@NgModule({
  declarations: [
    AppComponent,
    // MinContextLengthDirective,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
  ],
  providers: [],
  // exports: [
  //   MinContextLengthDirective
  // ],
  bootstrap: [AppComponent]
})
export class AppModule { }
