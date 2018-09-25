import { Component, OnInit, Input } from "@angular/core";
import { HttpClient } from '@angular/common/http';
import { AppConfig } from '@geonature_config/app.config';

@Component({
  selector: "pnx-cmr-nomenclature-display",
  templateUrl: "nomenclature_display.component.html"
})

export class NomenclatureDisplayComponent implements OnInit {
  public nomenclature_display: any;
  @Input() id_nomenclature: number;

  constructor(private _api: HttpClient) { }

  ngOnInit() {

    this._api.get<any>(`${AppConfig.API_ENDPOINT}/cmr/nomenclature_display/` + this.id_nomenclature)
    .subscribe(data => {
      this.nomenclature_display = data;
      console.log(data);
    })

  }
}
