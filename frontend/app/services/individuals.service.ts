import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { AppConfig } from "@geonature_config/app.config";

@Injectable()
export class IndividualsService {
  constructor(private _api: HttpClient) {}

  getAllIndividuals() {
    return this._api.get<any>(`${AppConfig.API_ENDPOINT}/cmr/individuals`);
  }

  getOneIndividual(id) {
    return this._api.get<any>(`${AppConfig.API_ENDPOINT}/cmr/individuals/${id}`);
  }

  deleteIndividual(id) {
    return this._api.delete(`${AppConfig.API_ENDPOINT}/cmr/individuals/${id}`);
  }

  postIndividuals(form) {
    return this._api.post(`${AppConfig.API_ENDPOINT}/cmr/individuals`, form);
  }

}
